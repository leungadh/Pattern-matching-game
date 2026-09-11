"""Generates the 18 original flat SVG tile icons into ../icons/.
Each icon uses a 100x100 viewBox with a transparent background (the tile supplies the card colour).
Run:  python3 tools/make_icons.py
"""
import math, os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

def petals(cx, cy, r, pr, n, fill):
    s = ""
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        s += f'<circle cx="{cx + r*math.cos(a):.1f}" cy="{cy + r*math.sin(a):.1f}" r="{pr}" fill="{fill}"/>'
    return s

ICONS = {
"01-apple": '''
<path d="M50 32 C38 22 16 26 16 50 C16 74 34 90 44 88 C47 87 53 87 56 88 C66 90 84 74 84 50 C84 26 62 22 50 32Z" fill="#E53935"/>
<path d="M50 32 Q50 20 56 11" stroke="#5D4037" stroke-width="4.5" fill="none" stroke-linecap="round"/>
<path d="M55 21 Q68 9 79 16 Q68 28 55 21Z" fill="#43A047"/>
<ellipse cx="31" cy="46" rx="5" ry="10" fill="#fff" opacity=".35"/>''',

"02-lemon": '''
<g transform="rotate(-25 50 52)">
<ellipse cx="50" cy="52" rx="33" ry="24" fill="#FDD835" stroke="#F9A825" stroke-width="3"/>
<ellipse cx="15" cy="52" rx="6" ry="5" fill="#FDD835" stroke="#F9A825" stroke-width="3"/>
<ellipse cx="85" cy="52" rx="6" ry="5" fill="#FDD835" stroke="#F9A825" stroke-width="3"/>
<ellipse cx="40" cy="43" rx="11" ry="4" fill="#fff" opacity=".5"/></g>
<path d="M66 20 Q82 10 90 21 Q78 31 66 20Z" fill="#7CB342"/>''',

"03-fish": '''
<path d="M68 50 L90 32 L86 50 L90 68Z" fill="#1565C0"/>
<ellipse cx="44" cy="50" rx="30" ry="20" fill="#1E88E5"/>
<path d="M40 32 Q50 18 60 34Z" fill="#1565C0"/>
<path d="M48 36 Q56 50 48 64" stroke="#90CAF9" stroke-width="3" fill="none"/>
<circle cx="28" cy="46" r="6" fill="#fff"/><circle cx="27" cy="46" r="3" fill="#0D1B2A"/>
<circle cx="12" cy="30" r="3.5" fill="none" stroke="#64B5F6" stroke-width="2"/>
<circle cx="18" cy="20" r="2.5" fill="none" stroke="#64B5F6" stroke-width="2"/>''',

"04-cat": '''
<path d="M22 44 L26 12 L46 30Z" fill="#FB8C00"/><path d="M78 44 L74 12 L54 30Z" fill="#FB8C00"/>
<path d="M28 34 L29 20 L39 29Z" fill="#F8BBD0"/><path d="M72 34 L71 20 L61 29Z" fill="#F8BBD0"/>
<circle cx="50" cy="56" r="31" fill="#FB8C00"/>
<path d="M38 28 L42 40 M50 26 L50 38 M62 28 L58 40" stroke="#E65100" stroke-width="3.5" stroke-linecap="round"/>
<ellipse cx="38" cy="54" rx="5" ry="7" fill="#212121"/><ellipse cx="62" cy="54" rx="5" ry="7" fill="#212121"/>
<circle cx="39.5" cy="52" r="1.8" fill="#fff"/><circle cx="63.5" cy="52" r="1.8" fill="#fff"/>
<path d="M45 64 L55 64 L50 70Z" fill="#EC407A"/>
<path d="M50 70 Q46 76 41 74 M50 70 Q54 76 59 74" stroke="#5D4037" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<path d="M30 66 L10 62 M30 71 L11 74 M70 66 L90 62 M70 71 L89 74" stroke="#5D4037" stroke-width="2" stroke-linecap="round"/>''',

"05-snowflake": '''
<g stroke="#00ACC1" stroke-width="6" stroke-linecap="round" fill="none">
''' + "".join(f'''<g transform="rotate({a} 50 50)"><path d="M50 10 L50 90 M50 24 L40 15 M50 24 L60 15 M50 76 L40 85 M50 76 L60 85"/></g>''' for a in (0, 60, 120)) + '''
</g><circle cx="50" cy="50" r="7" fill="#00ACC1"/><circle cx="50" cy="50" r="3" fill="#E0F7FA"/>''',

"06-tree": '''
<rect x="43" y="62" width="14" height="30" rx="3" fill="#6D4C41"/>
<circle cx="50" cy="32" r="21" fill="#43A047"/><circle cx="31" cy="50" r="18" fill="#43A047"/>
<circle cx="69" cy="50" r="18" fill="#43A047"/><circle cx="50" cy="55" r="19" fill="#388E3C"/>
<circle cx="42" cy="26" r="6" fill="#81C784" opacity=".8"/>
<circle cx="62" cy="42" r="3.5" fill="#E53935"/><circle cx="36" cy="56" r="3.5" fill="#E53935"/><circle cx="56" cy="62" r="3.5" fill="#E53935"/>''',

"07-flower": '''
<path d="M50 52 L50 94" stroke="#43A047" stroke-width="5" stroke-linecap="round"/>
<path d="M50 80 Q30 64 22 76 Q36 88 50 80Z" fill="#66BB6A"/>
''' + petals(50, 38, 19, 13, 6, "#EC407A") + '''
<circle cx="50" cy="38" r="12" fill="#FFD54F"/><circle cx="46" cy="35" r="3" fill="#FFF59D"/>''',

"08-mushroom": '''
<path d="M37 54 L63 54 L66 86 Q50 92 34 86Z" fill="#FFF3E0" stroke="#BCAAA4" stroke-width="2.5"/>
<path d="M10 58 Q10 14 50 14 Q90 14 90 58 Q50 50 10 58Z" fill="#BF5B2C"/>
<circle cx="32" cy="36" r="6" fill="#FFF3E0"/><circle cx="56" cy="26" r="5" fill="#FFF3E0"/>
<circle cx="70" cy="44" r="6.5" fill="#FFF3E0"/><circle cx="48" cy="44" r="3.5" fill="#FFF3E0"/>''',

"09-rocket": '''
<path d="M42 72 Q50 98 58 72Z" fill="#FFA000"/><path d="M46 72 Q50 88 54 72Z" fill="#FFEB3B"/>
<path d="M36 56 L20 80 L37 73Z" fill="#E53935"/><path d="M64 56 L80 80 L63 73Z" fill="#E53935"/>
<path d="M50 6 C68 22 70 52 64 74 L36 74 C30 52 32 22 50 6Z" fill="#ECEFF1" stroke="#78909C" stroke-width="3"/>
<path d="M50 6 C58 13 62 20 64 27 L36 27 C38 20 42 13 50 6Z" fill="#E53935"/>
<circle cx="50" cy="44" r="9" fill="#29B6F6" stroke="#546E7A" stroke-width="3"/>
<circle cx="47" cy="41" r="2.5" fill="#fff" opacity=".7"/>''',

"10-house": '''
<rect x="62" y="20" width="10" height="22" fill="#37474F"/>
<rect x="22" y="46" width="56" height="44" fill="#00897B"/>
<path d="M12 50 L50 16 L88 50Z" fill="#37474F"/>
<rect x="43" y="64" width="14" height="26" rx="2" fill="#FFCC80"/><circle cx="54" cy="78" r="1.8" fill="#6D4C41"/>
<rect x="28" y="56" width="11" height="11" fill="#FFF59D" stroke="#004D40" stroke-width="2"/>
<rect x="61" y="56" width="11" height="11" fill="#FFF59D" stroke="#004D40" stroke-width="2"/>''',

"11-key": '''
<circle cx="30" cy="50" r="17" fill="none" stroke="#F9A825" stroke-width="10"/>
<rect x="44" y="45" width="46" height="10" rx="3" fill="#F9A825"/>
<rect x="72" y="53" width="7" height="14" rx="1.5" fill="#F9A825"/><rect x="83" y="53" width="7" height="10" rx="1.5" fill="#F9A825"/>
<circle cx="25" cy="44" r="3" fill="#FFF59D"/>''',

"12-umbrella": '''
<path d="M50 50 L50 82 Q50 91 42 91 Q35 91 35 84" stroke="#4A148C" stroke-width="5.5" fill="none" stroke-linecap="round"/>
<path d="M50 29 L50 20" stroke="#4A148C" stroke-width="4" stroke-linecap="round"/>
<path d="M10 54 Q50 2 90 54 Q81 46 72 54 Q61 45 50 54 Q39 45 28 54 Q19 46 10 54Z" fill="#8E24AA"/>
<path d="M50 29 Q40 38 28 54 M50 29 Q60 38 72 54" stroke="#6A1B9A" stroke-width="2.5" fill="none"/>''',

"13-anchor": '''
<g stroke="#283593" stroke-width="7" fill="none" stroke-linecap="round">
<circle cx="50" cy="18" r="8"/><path d="M50 26 L50 86"/><path d="M33 40 L67 40"/>
<path d="M20 62 Q22 88 50 86 Q78 88 80 62"/></g>
<path d="M12 66 L20 52 L28 66Z" fill="#283593"/><path d="M72 66 L80 52 L88 66Z" fill="#283593"/>''',

"14-music": '''
<path d="M38 26 L80 16 L80 30 L38 40Z" fill="#212121"/>
<rect x="36" y="26" width="6" height="52" fill="#212121"/><rect x="74" y="16" width="6" height="52" fill="#212121"/>
<ellipse cx="29" cy="78" rx="13" ry="9.5" transform="rotate(-20 29 78)" fill="#212121"/>
<ellipse cx="67" cy="68" rx="13" ry="9.5" transform="rotate(-20 67 68)" fill="#212121"/>''',

"15-gift": '''
<rect x="20" y="46" width="60" height="42" rx="3" fill="#7CB342"/>
<rect x="15" y="34" width="70" height="15" rx="3" fill="#9CCC65"/>
<rect x="45" y="34" width="10" height="54" fill="#E53935"/>
<ellipse cx="38" cy="26" rx="13" ry="7" transform="rotate(20 38 26)" fill="none" stroke="#E53935" stroke-width="6"/>
<ellipse cx="62" cy="26" rx="13" ry="7" transform="rotate(-20 62 26)" fill="none" stroke="#E53935" stroke-width="6"/>
<circle cx="50" cy="33" r="5" fill="#C62828"/>''',

"16-storm": '''
<path d="M50 54 L38 78 L49 78 L42 97 L67 67 L55 67 L62 54Z" fill="#FFC107" stroke="#FF8F00" stroke-width="2" stroke-linejoin="round"/>
<circle cx="34" cy="42" r="16" fill="#90A4AE"/><circle cx="56" cy="32" r="21" fill="#90A4AE"/>
<circle cx="74" cy="46" r="14" fill="#90A4AE"/><rect x="20" y="42" width="66" height="18" rx="9" fill="#90A4AE"/>
<circle cx="50" cy="26" r="7" fill="#CFD8DC" opacity=".8"/>''',

"17-butterfly": '''
<ellipse cx="30" cy="34" rx="19" ry="22" transform="rotate(-25 30 34)" fill="#29B6F6"/>
<ellipse cx="70" cy="34" rx="19" ry="22" transform="rotate(25 70 34)" fill="#29B6F6"/>
<ellipse cx="33" cy="68" rx="14" ry="16" transform="rotate(25 33 68)" fill="#0288D1"/>
<ellipse cx="67" cy="68" rx="14" ry="16" transform="rotate(-25 67 68)" fill="#0288D1"/>
<circle cx="28" cy="32" r="6" fill="#FFEB3B"/><circle cx="72" cy="32" r="6" fill="#FFEB3B"/>
<rect x="46" y="26" width="8" height="54" rx="4" fill="#263238"/>
<path d="M48 27 Q42 12 34 10 M52 27 Q58 12 66 10" stroke="#263238" stroke-width="2.5" fill="none" stroke-linecap="round"/>''',

"18-icecream": '''
<path d="M30 50 L50 95 L70 50Z" fill="#D7A15A"/>
<path d="M36 58 L60 70 M40 70 L58 61 M44 82 L54 76 M34 54 L66 54" stroke="#A1662F" stroke-width="2.5"/>
<circle cx="50" cy="30" r="20" fill="#A5D6A7"/><circle cx="34" cy="46" r="11" fill="#A5D6A7"/>
<circle cx="50" cy="48" r="11" fill="#A5D6A7"/><circle cx="66" cy="46" r="11" fill="#A5D6A7"/>
<circle cx="50" cy="10" r="6" fill="#E53935"/><path d="M50 5 Q55 0 60 2" stroke="#43A047" stroke-width="2" fill="none"/>
<circle cx="42" cy="26" r="2" fill="#5D4037"/><circle cx="58" cy="34" r="2" fill="#5D4037"/><circle cx="48" cy="40" r="2" fill="#5D4037"/>''',
}

for name, body in ICONS.items():
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">{body.strip()}\n</svg>\n'
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)
print(f"wrote {len(ICONS)} icons to {os.path.abspath(OUT)}")
