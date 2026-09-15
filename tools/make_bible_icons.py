"""Generates 18 Bible-themed tile icons (100x100 SVG) into ../bible/icons/.
Each icon has its own main colour and shape so pairs are easy to spot from across a room.
Run:  python3 tools/make_bible_icons.py
"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "..", "bible", "icons")
os.makedirs(OUT, exist_ok=True)


def rays(cx, cy, r1, r2, n, col, w=4, rot=0):
    s = ""
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        s += (f'<line x1="{cx + r1*math.cos(a):.1f}" y1="{cy + r1*math.sin(a):.1f}" '
              f'x2="{cx + r2*math.cos(a):.1f}" y2="{cy + r2*math.sin(a):.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    return s


ICONS = {
"01-dove": '''
<circle cx="50" cy="50" r="44" fill="#E3F2FD"/>
<path d="M30 56 Q20 30 42 20 Q40 38 52 46Z" fill="#fff" stroke="#90A4AE" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M18 62 Q30 44 56 48 Q70 40 76 44 Q80 50 72 54 Q64 70 42 70 Q30 70 18 62Z" fill="#fff" stroke="#90A4AE" stroke-width="2.5"/>
<path d="M18 62 L8 56 L12 66Z" fill="#fff" stroke="#90A4AE" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M76 46 L86 48 L77 51Z" fill="#FFA000"/><circle cx="71" cy="46" r="2.2" fill="#263238"/>
<path d="M84 50 Q88 62 82 72" stroke="#558B2F" stroke-width="2.5" fill="none"/>
<ellipse cx="88" cy="60" rx="5" ry="2.6" fill="#7CB342" transform="rotate(60 88 60)"/>
<ellipse cx="80" cy="66" rx="5" ry="2.6" fill="#7CB342" transform="rotate(-30 80 66)"/>''',

"02-ark": '''
<path d="M6 82 q11 -8 22 0 q11 8 22 0 q11 -8 22 0 q11 8 22 0" stroke="#29B6F6" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M8 56 L92 56 L82 76 Q50 84 18 76Z" fill="#8D6E63"/>
<path d="M12 64 L88 64" stroke="#6D4C41" stroke-width="3"/>
<rect x="28" y="36" width="44" height="21" fill="#D7CCC8"/>
<path d="M22 38 L50 20 L78 38Z" fill="#C62828"/>
<rect x="36" y="43" width="9" height="8" fill="#5D4037"/><rect x="55" y="43" width="9" height="8" fill="#5D4037"/>''',

"03-rainbow": ''.join(
    f'<path d="M{50-r} 74 A{r} {r} 0 0 1 {50+r} 74" stroke="{c}" stroke-width="7.5" fill="none"/>'
    for r, c in zip((42, 35, 28, 21, 14), ("#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5"))) + '''
<ellipse cx="16" cy="76" rx="14" ry="8" fill="#fff" stroke="#CFD8DC" stroke-width="2"/>
<ellipse cx="84" cy="76" rx="14" ry="8" fill="#fff" stroke="#CFD8DC" stroke-width="2"/>''',

"04-tablets": '''
<path d="M10 88 L10 30 Q10 12 28 12 Q46 12 46 30 L46 88Z" fill="#B0BEC5" stroke="#607D8B" stroke-width="3"/>
<path d="M54 88 L54 30 Q54 12 72 12 Q90 12 90 30 L90 88Z" fill="#B0BEC5" stroke="#607D8B" stroke-width="3"/>
<g stroke="#546E7A" stroke-width="3.5" stroke-linecap="round">
<path d="M20 34 L36 34 M20 46 L36 46 M20 58 L36 58 M20 70 L36 70"/>
<path d="M64 34 L80 34 M64 46 L80 46 M64 58 L80 58 M64 70 L80 70"/></g>''',

"05-crown": '''
<path d="M12 74 L16 30 L34 50 L50 22 L66 50 L84 30 L88 74Z" fill="#FFC107" stroke="#FF8F00" stroke-width="3" stroke-linejoin="round"/>
<rect x="12" y="72" width="76" height="14" rx="3" fill="#FFB300" stroke="#FF8F00" stroke-width="3"/>
<circle cx="16" cy="28" r="5" fill="#FFC107"/><circle cx="50" cy="20" r="5" fill="#FFC107"/><circle cx="84" cy="28" r="5" fill="#FFC107"/>
<circle cx="30" cy="79" r="4.5" fill="#E53935"/><circle cx="50" cy="79" r="4.5" fill="#1E88E5"/><circle cx="70" cy="79" r="4.5" fill="#43A047"/>
<path d="M44 58 L50 50 L56 58 L50 66Z" fill="#E53935"/>''',

"06-harp": '''
<path d="M24 90 L24 14 Q60 14 80 40 Q70 50 72 90Z" fill="none" stroke="#A1662F" stroke-width="7" stroke-linejoin="round"/>
<path d="M24 14 Q60 14 80 40" stroke="#FFC107" stroke-width="7" fill="none" stroke-linecap="round"/>
<rect x="18" y="84" width="60" height="9" rx="4" fill="#8D5524"/>
<g stroke="#FFE082" stroke-width="2">''' + "".join(
    f'<line x1="{x}" y1="{17 + (x-24)*0.55 + ((x-24)/56)**2*14:.0f}" x2="{x}" y2="84"/>' for x in range(32, 74, 7)) + '''</g>
<circle cx="24" cy="14" r="6" fill="#FFC107"/>''',

"07-sling": '''
<path d="M20 12 Q30 44 46 58" stroke="#8D4E36" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M80 12 Q70 44 56 58" stroke="#8D4E36" stroke-width="4" fill="none" stroke-linecap="round"/>
<ellipse cx="51" cy="64" rx="15" ry="10" fill="#C62828"/>
<circle cx="51" cy="60" r="7" fill="#9E9E9E"/>
<circle cx="20" cy="12" r="5" fill="#FFCC80"/><circle cx="80" cy="12" r="5" fill="#FFCC80"/>
<ellipse cx="22" cy="86" rx="10" ry="7" fill="#9E9E9E"/><ellipse cx="42" cy="89" rx="8" ry="6" fill="#BDBDBD"/>
<ellipse cx="62" cy="87" rx="9" ry="6.5" fill="#9E9E9E"/><ellipse cx="80" cy="89" rx="7" ry="5" fill="#BDBDBD"/>''',

"08-bread": '''
<path d="M12 56 L88 56 L78 88 L22 88Z" fill="#D7A15A"/>
<g stroke="#A1662F" stroke-width="2.5"><path d="M16 66 L84 66 M19 76 L81 76"/>''' + "".join(
    f'<line x1="{x}" y1="56" x2="{x - (x-50)*0.25:.0f}" y2="88"/>' for x in range(22, 84, 12)) + '''</g>
<ellipse cx="32" cy="48" rx="18" ry="12" fill="#F4C27A" stroke="#C98B3A" stroke-width="2.5"/>
<ellipse cx="66" cy="48" rx="18" ry="12" fill="#F4C27A" stroke="#C98B3A" stroke-width="2.5"/>
<ellipse cx="49" cy="36" rx="18" ry="12" fill="#FFD08A" stroke="#C98B3A" stroke-width="2.5"/>
<path d="M40 34 L44 40 M49 32 L53 38 M58 34 L62 40" stroke="#C98B3A" stroke-width="2.5" stroke-linecap="round"/>''',

"09-star": '''
<circle cx="50" cy="50" r="44" fill="#1A237E"/>
<circle cx="22" cy="28" r="2" fill="#fff"/><circle cx="80" cy="30" r="1.8" fill="#fff"/><circle cx="26" cy="74" r="1.6" fill="#fff"/><circle cx="76" cy="76" r="2" fill="#fff"/>
<path d="M50 10 L57 43 L90 50 L57 57 L50 90 L43 57 L10 50 L43 43Z" fill="#FFEB3B"/>
<path d="M50 30 L54 46 L70 50 L54 54 L50 70 L46 54 L30 50 L46 46Z" fill="#fff" transform="rotate(45 50 50)"/>''',

"10-lamb": '''
<rect x="30" y="66" width="7" height="22" rx="3" fill="#5D4037"/><rect x="62" y="66" width="7" height="22" rx="3" fill="#5D4037"/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="15" fill="#FAFAFA" stroke="#E0E0E0" stroke-width="2"/>'
    for x, y in ((34, 52), (50, 44), (66, 52), (42, 64), (58, 64), (72, 42), (28, 40))) + '''
<ellipse cx="20" cy="46" rx="12" ry="14" fill="#FFE0E0" stroke="#E0BDBD" stroke-width="2"/>
<ellipse cx="11" cy="42" rx="7" ry="4" fill="#FFCDD2" transform="rotate(-30 11 42)"/>
<circle cx="17" cy="44" r="2.5" fill="#263238"/><path d="M16 53 Q20 55 23 53" stroke="#8D4E36" stroke-width="2" fill="none"/>
<circle cx="26" cy="32" r="8" fill="#FAFAFA" stroke="#E0E0E0" stroke-width="2"/>''',

"11-lion": '''
''' + "".join(f'<circle cx="{50 + 34*math.cos(a):.1f}" cy="{50 + 34*math.sin(a):.1f}" r="13" fill="#E65100"/>'
              for a in [2*math.pi*i/12 for i in range(12)]) + '''
<circle cx="50" cy="50" r="34" fill="#EF6C00"/>
<circle cx="50" cy="52" r="25" fill="#FFB74D"/>
<circle cx="31" cy="30" r="7" fill="#FFB74D"/><circle cx="69" cy="30" r="7" fill="#FFB74D"/>
<circle cx="41" cy="46" r="4" fill="#3E2723"/><circle cx="59" cy="46" r="4" fill="#3E2723"/>
<path d="M44 55 L56 55 L50 62Z" fill="#5D4037"/>
<path d="M50 62 Q45 68 40 65 M50 62 Q55 68 60 65" stroke="#5D4037" stroke-width="2.5" fill="none" stroke-linecap="round"/>''',

"12-burning-bush": '''
<path d="M50 8 Q70 28 62 44 Q76 36 74 22 Q92 44 76 64 L24 64 Q8 44 26 22 Q24 36 38 44 Q30 28 50 8Z" fill="#FF5722"/>
<path d="M50 24 Q62 38 56 50 Q66 44 66 36 Q76 52 64 64 L36 64 Q24 52 34 36 Q34 44 44 50 Q38 38 50 24Z" fill="#FFC107"/>
<path d="M50 40 Q56 48 52 58 L48 58 Q44 48 50 40Z" fill="#FFF59D"/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2E7D32"/>' for x, y, r in ((24, 72, 14), (40, 66, 14), (60, 66, 14), (76, 72, 14), (50, 78, 16), (32, 82, 12), (68, 82, 12))) + '''
<rect x="46" y="84" width="8" height="10" fill="#5D4037"/>''',

"13-oil-lamp": '''
<path d="M50 14 Q62 30 50 42 Q38 30 50 14Z" fill="#FF9800"/><path d="M50 24 Q56 32 50 40 Q44 32 50 24Z" fill="#FFF59D"/>
<path d="M14 60 Q14 48 40 48 L68 48 Q88 48 92 56 L78 60 Q84 76 50 78 Q14 76 14 60Z" fill="#BF5B2C"/>
<ellipse cx="46" cy="50" rx="10" ry="4" fill="#4E342E"/>
<path d="M16 58 Q4 54 8 46 Q14 50 22 52" stroke="#BF5B2C" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M30 66 Q50 72 70 66" stroke="#E8A07A" stroke-width="3" fill="none"/>
<rect x="38" y="78" width="24" height="8" rx="3" fill="#8D3E1A"/>''',

"14-scroll": '''
<rect x="22" y="18" width="56" height="64" fill="#FFF3D6" stroke="#C8A96A" stroke-width="2.5"/>
<g stroke="#8D6E63" stroke-width="3" stroke-linecap="round"><path d="M32 32 L68 32 M32 42 L64 42 M32 52 L68 52 M32 62 L60 62 M32 72 L66 72"/></g>
<rect x="14" y="10" width="72" height="12" rx="6" fill="#E6C88F" stroke="#A1662F" stroke-width="2.5"/>
<rect x="14" y="78" width="72" height="12" rx="6" fill="#E6C88F" stroke="#A1662F" stroke-width="2.5"/>
<circle cx="12" cy="16" r="5" fill="#8D5524"/><circle cx="88" cy="16" r="5" fill="#8D5524"/>
<circle cx="12" cy="84" r="5" fill="#8D5524"/><circle cx="88" cy="84" r="5" fill="#8D5524"/>''',

"15-grapes": '''
<path d="M50 20 Q52 10 60 6" stroke="#6D4C41" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M54 16 Q72 4 84 16 Q70 26 54 16Z" fill="#7CB342"/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="10.5" fill="#7B1FA2"/><circle cx="{x-3}" cy="{y-3}" r="3" fill="#CE93D8" opacity=".8"/>'
    for x, y in ((24, 30), (44, 28), (64, 30), (80, 36), (34, 46), (54, 46), (72, 50),
                 (42, 63), (62, 64), (52, 80))),

"16-wheat": '''
<g stroke="#A1662F" stroke-width="3">''' + "".join(
    f'<path d="M50 92 Q{50+dx*0.3:.0f} 60 {50+dx} {30 + abs(dx)*0.4:.0f}" fill="none"/>' for dx in (-24, -12, 0, 12, 24)) + '</g>' + "".join(
    "".join(f'<ellipse cx="{50+dx + (k%2*2-1)*4:.0f}" cy="{30 + abs(dx)*0.4 - 16 + k*6:.0f}" rx="4" ry="7" fill="#FBC02D" '
            f'transform="rotate({(k%2*2-1)*25} {50+dx + (k%2*2-1)*4:.0f} {30 + abs(dx)*0.4 - 16 + k*6:.0f})"/>' for k in range(6))
    for dx in (-24, -12, 0, 12, 24)) + '''
<path d="M36 72 Q50 66 64 72 L62 80 Q50 74 38 80Z" fill="#C62828"/>''',

"17-cross": '''
<circle cx="50" cy="44" r="40" fill="#FFE0B2"/>''' + rays(50, 44, 26, 40, 12, "#FFB74D", 4) + '''
<path d="M4 94 Q50 66 96 94Z" fill="#66BB6A"/>
<rect x="44" y="16" width="12" height="66" rx="2" fill="#6D4C41"/>
<rect x="28" y="30" width="44" height="11" rx="2" fill="#6D4C41"/>
<path d="M47 20 L47 78 M31 34 L69 34" stroke="#8D6E63" stroke-width="2.5"/>''',

"18-big-fish": '''
<path d="M72 50 L94 30 L90 50 L94 70Z" fill="#3949AB"/>
<path d="M8 52 Q14 22 46 22 Q72 22 76 50 Q72 78 46 78 Q14 78 8 52Z" fill="#5C6BC0"/>
<path d="M14 58 Q40 74 72 58 Q60 76 40 76 Q20 74 14 58Z" fill="#9FA8DA"/>
<path d="M8 52 L26 46 L26 56Z" fill="#283593"/>
<circle cx="28" cy="40" r="6" fill="#fff"/><circle cx="27" cy="41" r="3" fill="#1A1A2E"/>
<path d="M44 22 Q44 8 38 4 M44 22 Q46 8 52 4" stroke="#81D4FA" stroke-width="3.5" fill="none" stroke-linecap="round"/>''',
}

if __name__ == "__main__":
    for name, body in ICONS.items():
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">{body.strip()}\n</svg>\n'
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(svg)
    print(f"wrote {len(ICONS)} icons to {os.path.abspath(OUT)}")
