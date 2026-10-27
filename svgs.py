# -*- coding: utf-8 -*-
SVG_RIVER = '''<svg viewBox="0 0 936 360" style="width:100%;display:block;border-radius:4px">
<rect width="936" height="360" rx="4" fill="#0C0F14"/>
<defs><linearGradient id="dusk" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#1A2230"/><stop offset="1" stop-color="#3A2A22"/></linearGradient></defs>
<rect width="936" height="150" fill="url(#dusk)"/>
<circle cx="812" cy="138" r="46" fill="#FF4B1F" opacity="0.5"/>
<path d="M0 150H936" stroke="#232C3A"/>
<path d="M0 216 Q 288 196 540 212 T 936 202 L936 360 L0 360 Z" fill="#111A26"/>
<g stroke="#2B3443" stroke-width="5" fill="none">
<path d="M172 184 V252"/><path d="M110 196 H236"/>
<path d="M594 178 V248"/><path d="M534 190 H656"/></g>
<text x="172" y="172" text-anchor="middle" font-family="Liberation Mono,monospace" font-size="15" letter-spacing="2" fill="#6B7079">JAMSU</text>
<text x="594" y="166" text-anchor="middle" font-family="Liberation Mono,monospace" font-size="15" letter-spacing="2" fill="#6B7079">HANGANG</text>
<path d="M110 298 C 270 286, 432 304, 594 288 S 792 268, 846 262" stroke="#D4FF36" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.08"/>
<path d="M110 298 C 270 286, 432 304, 594 288 S 792 268, 846 262" stroke="#D4FF36" stroke-width="5" fill="none" stroke-linecap="round"/>
<circle cx="110" cy="298" r="11" fill="#0C0F14" stroke="#D4FF36" stroke-width="4.5"/>
<circle cx="846" cy="262" r="12" fill="#D4FF36"/>
<text x="110" y="336" font-family="Liberation Mono,monospace" font-size="17" letter-spacing="2.4" fill="#97A1B0">START · BANPO</text>
<text x="846" y="300" text-anchor="end" font-family="Liberation Mono,monospace" font-size="17" letter-spacing="2.4" fill="#D4FF36">TURN · NODEULSEOM</text>
<text x="468" y="86" text-anchor="middle" font-family="Liberation Mono,monospace" font-size="17" letter-spacing="3.4" fill="#97A1B0">SUNSET 19:10 · RUN WEST, RETURN UNDER THE LIGHTS</text></svg>'''
SVG_MTN = '''<svg viewBox="0 0 936 360" style="width:100%;display:block;border-radius:4px">
<rect width="936" height="360" rx="4" fill="#0C0F14"/>
<defs><linearGradient id="mt" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#D4FF36" stop-opacity="0.30"/>
<stop offset="1" stop-color="#D4FF36" stop-opacity="0"/></linearGradient></defs>
<g stroke="#161C25" stroke-width="1.5"><path d="M86 286H896"/><path d="M86 198H896"/><path d="M86 110H896"/></g>
<g font-family="Liberation Mono,monospace" font-size="15" letter-spacing="2" fill="#49515C" text-anchor="end">
<text x="70" y="292">0M</text><text x="70" y="204">120M</text><text x="70" y="116">240M</text></g>
<path d="M86 286 L206 272 L318 232 L432 162 L532 112 L604 98 L700 170 L792 228 L896 286 Z" fill="url(#mt)"/>
<path d="M86 286 L206 272 L318 232 L432 162 L532 112 L604 98 L700 170 L792 228 L896 286"
 fill="none" stroke="#D4FF36" stroke-width="5" stroke-linejoin="round"/>
<g transform="translate(604,94) scale(1.25)">
<path d="M-9 0 L-3 -24 L3 -24 L9 0 Z" fill="#D4FF36"/>
<rect x="-3" y="-42" width="6" height="18" fill="#D4FF36"/>
<path d="M-10 -42 L10 -42 L7 -52 L-7 -52 Z" fill="#D4FF36"/>
<path d="M0 -52 L0 -74" stroke="#D4FF36" stroke-width="3"/>
<circle cx="0" cy="-78" r="4.5" fill="#FF4B1F"/></g>
<text x="604" y="36" text-anchor="middle" font-family="Liberation Mono,monospace" font-size="18" letter-spacing="3" fill="#D4FF36">N SEOUL TOWER · THE TOP</text>
<g font-family="Liberation Mono,monospace" font-size="17" letter-spacing="2.4" fill="#6B7079">
<text x="86" y="324">START</text><text x="896" y="324" text-anchor="end">FINISH</text></g></svg>'''
SVG_CITY = '''<svg viewBox="0 0 936 360" style="width:100%;display:block;border-radius:4px">
<rect width="936" height="360" rx="4" fill="#0C0F14"/>
<g stroke="#161C25" stroke-width="1.5">
<path d="M0 90H936"/><path d="M0 180H936"/><path d="M0 270H936"/>
<path d="M234 0V360"/><path d="M468 0V360"/><path d="M702 0V360"/></g>
<path d="M155 296 L155 184 L270 84 L540 63 L774 101 L814 216 L684 305 L155 296"
 fill="none" stroke="#D4FF36" stroke-width="20" stroke-linejoin="round" opacity="0.07"/>
<path d="M155 296 L155 184 L270 84 L540 63 L774 101 L814 216 L684 305 L155 296"
 fill="none" stroke="#D4FF36" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M155 296 L155 184 L270 84 L540 63" fill="none" stroke="#FF4B1F" stroke-width="5" stroke-linejoin="round" stroke-dasharray="12 10"/>
<g fill="#0C0F14" stroke="#D4FF36" stroke-width="4">
<circle cx="774" cy="101" r="9"/><circle cx="814" cy="216" r="9"/><circle cx="684" cy="305" r="9"/></g>
<g fill="#D4FF36"><circle cx="270" cy="84" r="9"/><circle cx="540" cy="63" r="9"/></g>
<circle cx="155" cy="296" r="13" fill="#FAF8F4"/>
<g font-family="Liberation Mono,monospace" font-size="15" letter-spacing="2" fill="#A8AEB8">
<text x="155" y="334" text-anchor="middle">START / FINISH</text>
<text x="120" y="178" text-anchor="end">GYEONGBOK</text>
<text x="266" y="66" text-anchor="middle">CHEONGWADAE</text>
<text x="550" y="46">SAMCHEONG</text><text x="796" y="90">BUKCHON</text>
<text x="834" y="222">JONGMYO</text><text x="692" y="330">CHEONGGYE</text></g>
<text x="360" y="236" font-family="Liberation Mono,monospace" font-size="16" letter-spacing="2.4" fill="#FF7A64">JOY SHORTCUT · 4 KM</text></svg>'''