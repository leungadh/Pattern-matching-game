"""Generates the non-Bible answer pictures (800x800 SVG) into ../answers/backup/ (not used by the game).
Each scene is drawn so the subject spreads across the whole board, which keeps early reveals fair.
Run:  python3 tools/make_answers.py
"""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "answers", "backup")
os.makedirs(OUT, exist_ok=True)
R = random.Random(7)  # fixed seed -> same pictures every run


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">'
            f'<defs>{defs}</defs>{body}</svg>\n')


def vgrad(id, *stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="0" y2="1">{s}</linearGradient>'


def cloud(x, y, s=1.0, fill="#fff", op=1):
    return (f'<g fill="{fill}" opacity="{op}" transform="translate({x} {y}) scale({s})">'
            '<ellipse cx="0" cy="0" rx="70" ry="26"/><ellipse cx="-30" cy="-16" rx="36" ry="26"/>'
            '<ellipse cx="22" cy="-22" rx="42" ry="32"/></g>')


def birds(pts, col="#263238"):
    return "".join(f'<path d="M{x} {y} q12 -12 24 0 q12 -12 24 0" stroke="{col}" stroke-width="5" '
                   f'fill="none" stroke-linecap="round"/>' for x, y in pts)


def castle():
    d = vgrad("sky", (0, "#81D4FA"), (1, "#E1F5FE")) + vgrad("wall", (0, "#B0BEC5"), (1, "#78909C"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="680" cy="110" r="50" fill="#FFF176"/>'
    b += cloud(150, 120) + cloud(560, 210, .8)
    b += '<path d="M0 620 Q200 560 400 600 T800 590 L800 800 L0 800Z" fill="#7CB342"/>'
    b += '<path d="M0 700 Q300 650 800 700 L800 800 L0 800Z" fill="#558B2F"/>'
    # moat
    b += '<path d="M120 640 Q400 690 680 640 L700 690 Q400 740 100 690Z" fill="#4FC3F7"/>'

    def battlements(x, y, w, n):
        cw = w / (2 * n - 1)
        return "".join(f'<rect x="{x + i*2*cw:.1f}" y="{y - 22}" width="{cw:.1f}" height="24" fill="url(#wall)"/>' for i in range(n))
    # main wall
    b += '<rect x="170" y="400" width="460" height="250" fill="url(#wall)"/>' + battlements(170, 400, 460, 12)
    # keep
    b += '<rect x="300" y="250" width="200" height="160" fill="url(#wall)"/>' + battlements(300, 250, 200, 6)
    # towers
    for tx in (120, 580):
        b += f'<rect x="{tx}" y="300" width="100" height="350" fill="url(#wall)"/>'
        b += f'<path d="M{tx-10} 302 L{tx+50} 170 L{tx+110} 302Z" fill="#C62828"/>'
        b += f'<line x1="{tx+50}" y1="172" x2="{tx+50}" y2="120" stroke="#37474F" stroke-width="5"/>'
        b += f'<path d="M{tx+52} 122 L{tx+95} 136 L{tx+52} 150Z" fill="#FFD600"/>'
        b += f'<rect x="{tx+38}" y="380" width="24" height="44" rx="12" fill="#263238"/>'
    b += '<path d="M390 252 L400 140 L410 252Z" fill="#37474F"/><path d="M402 142 L450 158 L402 174Z" fill="#1E88E5"/>'
    # gate + windows
    b += '<path d="M345 650 L345 540 Q400 480 455 540 L455 650Z" fill="#4E342E"/>'
    b += '<g stroke="#3E2723" stroke-width="4">' + "".join(f'<line x1="{x}" y1="520" x2="{x}" y2="650"/>' for x in range(360, 455, 18)) + '</g>'
    for wx in (340, 440):
        b += f'<rect x="{wx}" y="300" width="22" height="40" rx="11" fill="#263238"/>'
    for wx in (230, 540):
        b += f'<rect x="{wx}" y="460" width="26" height="46" rx="13" fill="#263238"/>'
    b += '<path d="M345 650 L455 650 L470 700 L330 700Z" fill="#8D6E63"/>'
    b += birds([(250, 190), (300, 160)])
    return svg(b, d)


def pirate_ship():
    d = vgrad("sky", (0, "#FFB74D"), (.6, "#FFE0B2"), (1, "#FFF3E0")) + vgrad("sea", (0, "#0288D1"), (1, "#01579B"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="130" cy="150" r="60" fill="#FFF8E1"/>'
    b += cloud(620, 110, .9) + cloud(260, 70, .6)
    b += '<rect y="560" width="800" height="240" fill="url(#sea)"/>'
    # masts
    for mx, top in ((250, 150), (420, 90), (580, 170)):
        b += f'<rect x="{mx-7}" y="{top}" width="14" height="{580-top}" fill="#4E342E"/>'
    # sails
    def sail(mx, y, w, h):
        return (f'<path d="M{mx-w/2} {y} Q{mx} {y+14} {mx+w/2} {y} L{mx+w/2-8} {y+h} '
                f'Q{mx} {y+h+26} {mx-w/2+8} {y+h}Z" fill="#FFF8E1" stroke="#BCAAA4" stroke-width="3"/>')
    b += sail(250, 200, 150, 110) + sail(250, 330, 170, 120)
    b += sail(420, 140, 180, 120) + sail(420, 280, 200, 140)
    b += sail(580, 220, 140, 100) + sail(580, 340, 160, 110)
    b += '<path d="M420 92 L500 110 L420 128Z" fill="#212121"/>'
    b += '<circle cx="452" cy="110" r="7" fill="#fff"/>'
    # hull
    b += '<path d="M90 520 L710 520 L660 650 Q400 690 150 650Z" fill="#6D4C41"/>'
    b += '<path d="M90 520 L710 520 L700 548 L100 548Z" fill="#8D6E63"/>'
    b += '<path d="M60 470 L140 520 L100 548Z" fill="#6D4C41"/>'
    b += '<path d="M140 520 L30 440" stroke="#4E342E" stroke-width="8"/>'
    b += '<path d="M120 585 L680 585" stroke="#FFD54F" stroke-width="6"/>'
    b += "".join(f'<circle cx="{x}" cy="612" r="11" fill="#3E2723"/>' for x in range(200, 640, 80))
    # waves
    b += '<g stroke="#81D4FA" stroke-width="6" fill="none" stroke-linecap="round">'
    for y in (680, 730, 770):
        for x in range(-20, 820, 110):
            b += f'<path d="M{x + (y % 3) * 25} {y} q27 -18 55 0 q27 18 55 0"/>'
    b += '</g>' + birds([(640, 260), (690, 230)], "#5D4037")
    return svg(b, d)


def windmill():
    d = vgrad("sky", (0, "#90CAF9"), (1, "#E3F2FD"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>' + cloud(140, 140) + cloud(640, 260, .8)
    b += '<rect y="560" width="800" height="240" fill="#8BC34A"/>'
    cols = ["#E53935", "#FDD835", "#EC407A", "#FB8C00", "#AB47BC"]
    for i in range(7):
        y0 = 590 + i * 32
        b += f'<path d="M0 {y0} L800 {y0-40} L800 {y0-18} L0 {y0+22}Z" fill="{cols[i % 5]}"/>'
    # body
    b += '<path d="M330 600 L360 330 L440 330 L470 600Z" fill="#8D6E63"/>'
    b += '<path d="M340 335 Q400 250 460 335Z" fill="#5D4037"/>'
    b += '<rect x="380" y="530" width="40" height="70" rx="20" fill="#3E2723"/>'
    b += '<rect x="385" y="420" width="30" height="36" fill="#FFF59D" stroke="#3E2723" stroke-width="4"/>'
    b += '<rect x="320" y="470" width="160" height="12" fill="#4E342E"/>'
    # blades
    cx, cy = 400, 320
    for a in (20, 110, 200, 290):
        b += f'<g transform="rotate({a} {cx} {cy})"><rect x="{cx-6}" y="{cy-290}" width="12" height="290" fill="#4E342E"/>'
        b += f'<rect x="{cx+6}" y="{cy-280}" width="60" height="230" fill="#FFF8E1" stroke="#6D4C41" stroke-width="3"/>'
        for k in range(1, 6):
            b += f'<line x1="{cx+6}" y1="{cy-280+k*38}" x2="{cx+66}" y2="{cy-280+k*38}" stroke="#6D4C41" stroke-width="2"/>'
        b += '</g>'
    b += f'<circle cx="{cx}" cy="{cy}" r="18" fill="#3E2723"/>'
    return svg(b, d)


def snowman():
    d = vgrad("sky", (0, "#0D1B3E"), (1, "#3949AB"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="650" cy="120" r="50" fill="#FFF9C4"/>'
    b += '<circle cx="672" cy="108" r="46" fill="#1A2657"/>'
    for _ in range(70):
        b += f'<circle cx="{R.randint(0,800)}" cy="{R.randint(0,620)}" r="{R.choice([3,4,5,6])}" fill="#fff" opacity="{R.choice([.6,.8,1])}"/>'
    b += '<path d="M0 600 Q200 540 400 590 T800 570 L800 800 L0 800Z" fill="#E3F2FD"/>'
    b += '<path d="M0 680 Q400 620 800 690 L800 800 L0 800Z" fill="#fff"/>'
    # pine trees
    for tx, s in ((90, 1.1), (720, 1.0), (640, .7)):
        b += f'<g transform="translate({tx} 600) scale({s})"><rect x="-10" y="-20" width="20" height="40" fill="#4E342E"/>'
        b += '<path d="M-70 -20 L0 -140 L70 -20Z M-55 -90 L0 -200 L55 -90Z" fill="#1B5E20"/></g>'
    # snowman
    b += '<circle cx="400" cy="610" r="130" fill="#FAFAFA" stroke="#CFD8DC" stroke-width="4"/>'
    b += '<circle cx="400" cy="420" r="95" fill="#FAFAFA" stroke="#CFD8DC" stroke-width="4"/>'
    b += '<circle cx="400" cy="270" r="72" fill="#FAFAFA" stroke="#CFD8DC" stroke-width="4"/>'
    b += '<rect x="330" y="200" width="140" height="18" rx="6" fill="#212121"/><rect x="350" y="110" width="100" height="95" rx="6" fill="#212121"/>'
    b += '<rect x="350" y="180" width="100" height="16" fill="#C62828"/>'
    b += '<circle cx="375" cy="258" r="9" fill="#212121"/><circle cx="425" cy="258" r="9" fill="#212121"/>'
    b += '<path d="M400 275 L470 290 L400 292Z" fill="#FB8C00"/>'
    b += "".join(f'<circle cx="{x}" cy="{312 - abs(x-400)*0.15:.0f}" r="5" fill="#212121"/>' for x in (365, 383, 400, 417, 435))
    b += '<path d="M330 335 Q400 370 470 335 L470 360 Q400 395 330 360Z" fill="#C62828"/>'
    b += '<path d="M440 355 L470 450 L440 455 L420 365Z" fill="#C62828"/>'
    b += "".join(f'<circle cx="400" cy="{y}" r="11" fill="#212121"/>' for y in (400, 450, 560, 620))
    b += '<g stroke="#5D4037" stroke-width="9" stroke-linecap="round" fill="none">'
    b += '<path d="M315 410 L170 330 M220 358 L200 310"/><path d="M485 410 L630 320 M590 345 L620 300"/></g>'
    return svg(b, d)


def volcano():
    d = vgrad("sky", (0, "#4A148C"), (.5, "#D84315"), (1, "#FFB74D")) + vgrad("lava", (0, "#FFEB3B"), (1, "#FF5722"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    # smoke
    for x, y, r in ((400, 150, 90), (320, 110, 70), (490, 90, 80), (560, 170, 60), (250, 190, 55), (400, 60, 70)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#455A64" opacity=".85"/>'
    b += '<rect y="620" width="800" height="180" fill="#0277BD"/>'
    b += '<path d="M60 640 L330 250 L470 250 L740 640Z" fill="#4E342E"/>'
    b += '<path d="M330 250 L470 250 L520 330 L280 330Z" fill="#3E2723"/>'
    b += '<path d="M360 250 Q400 230 440 250 L470 330 Q450 420 480 520 L440 520 Q420 420 405 360 Q380 460 350 560 L320 560 Q350 440 350 330Z" fill="url(#lava)"/>'
    b += '<path d="M400 240 Q370 180 330 140 Q390 170 400 120 Q420 170 480 130 Q430 190 400 240Z" fill="url(#lava)"/>'
    for x, y in ((250, 90), (560, 70), (300, 40), (520, 150)):
        b += f'<circle cx="{x}" cy="{y}" r="12" fill="#FF7043"/>'
    # island + palms
    b += '<path d="M0 640 Q200 600 400 650 T800 630 L800 680 L0 680Z" fill="#FFE082"/>'
    for px, lean in ((120, -1), (690, 1)):
        b += f'<path d="M{px} 650 Q{px + lean*20} 560 {px + lean*50} 480" stroke="#6D4C41" stroke-width="16" fill="none" stroke-linecap="round"/>'
        tx, ty = px + lean * 50, 480
        for a in (-150, -110, -60, -20, 30):
            ang = math.radians(a)
            ex, ey = tx + 90 * math.cos(ang), ty + 90 * math.sin(ang) + 30
            b += f'<path d="M{tx} {ty} Q{(tx+ex)/2:.0f} {ty-40} {ex:.0f} {ey:.0f}" stroke="#2E7D32" stroke-width="18" fill="none" stroke-linecap="round"/>'
    b += '<g stroke="#4FC3F7" stroke-width="5" fill="none" stroke-linecap="round">'
    b += "".join(f'<path d="M{x} 730 q25 -14 50 0 q25 14 50 0"/>' for x in (60, 330, 590)) + '</g>'
    return svg(b, d)


def steam_train():
    d = vgrad("sky", (0, "#80DEEA"), (1, "#E0F7FA"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>' + cloud(640, 110, .9)
    b += '<path d="M0 470 Q180 380 360 450 T800 420 L800 800 L0 800Z" fill="#9CCC65"/>'
    b += '<path d="M0 620 L800 620 L800 800 L0 800Z" fill="#7CB342"/>'
    # smoke puffs
    for i, (x, y, r) in enumerate(((600, 250, 38), (540, 190, 48), (460, 140, 56), (360, 110, 62), (250, 100, 66), (130, 110, 60))):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ECEFF1" stroke="#B0BEC5" stroke-width="3"/>'
    # tracks
    b += '<rect x="0" y="628" width="800" height="12" fill="#5D4037"/>'
    b += "".join(f'<rect x="{x}" y="640" width="24" height="16" fill="#6D4C41"/>' for x in range(0, 800, 50))
    # carriages
    for cx, col in ((30, "#1E88E5"), (220, "#43A047")):
        b += f'<rect x="{cx}" y="440" width="170" height="150" rx="10" fill="{col}"/>'
        b += f'<rect x="{cx-6}" y="428" width="182" height="20" rx="6" fill="#37474F"/>'
        b += "".join(f'<rect x="{cx+18+k*52}" y="465" width="36" height="44" rx="5" fill="#FFF59D"/>' for k in range(3))
        b += "".join(f'<circle cx="{cx+wx}" cy="600" r="26" fill="#212121"/><circle cx="{cx+wx}" cy="600" r="10" fill="#9E9E9E"/>' for wx in (40, 130))
        b += f'<rect x="{cx+170}" y="560" width="20" height="10" fill="#37474F"/>'
    # locomotive
    b += '<rect x="410" y="370" width="150" height="220" rx="8" fill="#C62828"/>'
    b += '<rect x="400" y="355" width="170" height="24" rx="6" fill="#212121"/>'
    b += '<rect x="435" y="400" width="100" height="70" rx="6" fill="#FFF59D"/>'
    b += '<rect x="560" y="450" width="190" height="140" rx="60" fill="#212121"/>'
    b += '<rect x="620" y="370" width="36" height="90" fill="#212121"/><rect x="608" y="350" width="60" height="24" rx="6" fill="#424242"/>'
    b += '<circle cx="700" cy="400" r="16" fill="#FFD600"/>'
    b += '<rect x="560" y="500" width="190" height="10" fill="#FFD600"/>'
    b += '<path d="M750 560 L790 600 L750 600Z" fill="#9E9E9E"/>'
    for wx, r in ((470, 36), (600, 30), (690, 30)):
        b += f'<circle cx="{wx}" cy="{606 - r + 26}" r="{r}" fill="#212121"/><circle cx="{wx}" cy="{606 - r + 26}" r="{r*0.4:.0f}" fill="#E53935"/>'
    b += '<rect x="470" y="596" width="220" height="10" rx="5" fill="#9E9E9E"/>'
    return svg(b, d)


def octopus():
    d = vgrad("sea", (0, "#26C6DA"), (1, "#01579B"))
    b = '<rect width="800" height="800" fill="url(#sea)"/>'
    for x in range(0, 800, 90):
        b += f'<path d="M{x} 0 L{x+40} 0 L{x+160} 800 L{x+120} 800Z" fill="#fff" opacity=".05"/>'
    b += '<path d="M0 700 Q200 650 400 700 T800 690 L800 800 L0 800Z" fill="#FFE082"/>'
    for sx in (60, 140, 700, 750):
        b += f'<path d="M{sx} 720 Q{sx-30} 600 {sx+10} 500 Q{sx+40} 600 {sx+20} 720Z" fill="#2E7D32"/>'
    # tentacles spreading across the board
    col = "#8E24AA"
    ends = [(50, 470), (110, 640), (230, 690), (350, 700), (450, 700), (570, 690), (690, 640), (750, 470)]
    for i, (ex, ey) in enumerate(ends):
        side = ex - 400
        mx, my = 400 + side * 0.9, 560 - abs(side) * 0.25   # bend outward so the arms fan across the board
        b += f'<path d="M400 400 Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}" stroke="{col}" stroke-width="{46 - i % 2 * 6}" fill="none" stroke-linecap="round"/>'
        for t in (.55, .7, .85):
            px = (1-t)**2*400 + 2*(1-t)*t*mx + t*t*ex
            py = (1-t)**2*400 + 2*(1-t)*t*my + t*t*ey
            b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="#F3E5F5"/>'
    b += f'<ellipse cx="400" cy="300" rx="150" ry="170" fill="{col}"/>'
    b += '<ellipse cx="350" cy="220" rx="40" ry="60" fill="#fff" opacity=".2"/>'
    b += '<ellipse cx="345" cy="340" rx="32" ry="38" fill="#fff"/><ellipse cx="455" cy="340" rx="32" ry="38" fill="#fff"/>'
    b += '<circle cx="352" cy="348" r="16" fill="#1A1A2E"/><circle cx="448" cy="348" r="16" fill="#1A1A2E"/>'
    b += '<circle cx="357" cy="342" r="5" fill="#fff"/><circle cx="453" cy="342" r="5" fill="#fff"/>'
    b += '<path d="M370 410 Q400 435 430 410" stroke="#4A148C" stroke-width="7" fill="none" stroke-linecap="round"/>'
    b += '<circle cx="300" cy="390" r="16" fill="#F48FB1" opacity=".7"/><circle cx="500" cy="390" r="16" fill="#F48FB1" opacity=".7"/>'
    for _ in range(14):
        x, y, r = R.randint(40, 760), R.randint(30, 560), R.randint(6, 16)
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#E0F7FA" stroke-width="3" opacity=".8"/>'
    b += '<g transform="translate(640 150)"><ellipse rx="40" ry="22" fill="#FFB300"/><path d="M36 0 L66 -20 L66 20Z" fill="#FFB300"/><circle cx="-18" cy="-5" r="5" fill="#212121"/></g>'
    return svg(b, d)


def pyramids():
    d = vgrad("sky", (0, "#FF8A65"), (.55, "#FFCC80"), (1, "#FFE0B2"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="640" cy="170" r="80" fill="#FFF3E0"/>'
    b += '<path d="M0 560 Q250 520 500 560 T800 540 L800 800 L0 800Z" fill="#F4C27A"/>'
    for (cx, base, h, w) in ((230, 600, 340, 420), (520, 590, 280, 360), (720, 600, 160, 220)):
        b += f'<path d="M{cx-w/2} {base} L{cx} {base-h} L{cx+w/2} {base}Z" fill="#E0A458"/>'
        b += f'<path d="M{cx} {base-h} L{cx+w/2} {base} L{cx+w*0.12} {base}Z" fill="#B97A3A"/>'
        for k in range(1, 7):
            y = base - h * k / 7
            half = w / 2 * (1 - k / 7)
            b += f'<line x1="{cx-half:.0f}" y1="{y:.0f}" x2="{cx+half*0.24:.0f}" y2="{y:.0f}" stroke="#C98E4A" stroke-width="3"/>'
    b += '<path d="M0 640 Q300 600 800 650 L800 800 L0 800Z" fill="#EDB96A"/>'
    # camel + rider silhouette
    b += ('<g fill="#5D4037" transform="translate(470 690)">'
          '<path d="M-90 -40 Q-80 -110 -30 -100 Q0 -150 40 -100 Q70 -110 80 -70 L110 -110 Q130 -120 140 -100 L150 -90 L130 -85 L100 -40 Q90 -20 70 -30 L60 0 L50 0 L52 -30 L-40 -30 L-48 0 L-58 0 L-56 -32 Q-80 -30 -90 -40Z"/>'
          '<rect x="-72" y="-30" width="9" height="30"/><rect x="36" y="-30" width="9" height="30"/></g>')
    b += '<g transform="translate(90 640)"><path d="M0 0 Q10 -80 30 -150" stroke="#6D4C41" stroke-width="12" fill="none"/>'
    for a in (-160, -120, -60, -20):
        ang = math.radians(a)
        b += f'<path d="M30 -150 Q{30+40*math.cos(ang):.0f} {-190:.0f} {30+80*math.cos(ang):.0f} {-150+70*math.sin(ang)+40:.0f}" stroke="#388E3C" stroke-width="14" fill="none" stroke-linecap="round"/>'
    b += '</g>' + birds([(380, 150), (430, 120)], "#6D4C41")
    return svg(b, d)


def birthday_cake():
    d = vgrad("wall", (0, "#F8BBD0"), (1, "#FCE4EC"))
    b = '<rect width="800" height="800" fill="url(#wall)"/>'
    # bunting
    b += '<path d="M0 60 Q400 170 800 60" stroke="#6D4C41" stroke-width="4" fill="none"/>'
    cols = ["#E53935", "#FDD835", "#43A047", "#1E88E5", "#8E24AA"]
    for i in range(11):
        x = 30 + i * 70
        y = 60 + 110 * (1 - ((x - 400) / 400) ** 2) * 0.95
        b += f'<path d="M{x-24} {y-4:.0f} L{x+24} {y-4:.0f} L{x} {y+44:.0f}Z" fill="{cols[i % 5]}"/>'
    # balloons
    for x, y, c in ((90, 300, "#E53935"), (170, 250, "#1E88E5"), (650, 260, "#FDD835"), (720, 330, "#43A047")):
        b += f'<path d="M{x} {y+62} Q{x+20} {y+150} {x-5} {y+260}" stroke="#757575" stroke-width="3" fill="none"/>'
        b += f'<ellipse cx="{x}" cy="{y}" rx="50" ry="62" fill="{c}"/><ellipse cx="{x-18}" cy="{y-22}" rx="10" ry="18" fill="#fff" opacity=".4"/>'
    # table
    b += '<rect y="640" width="800" height="160" fill="#8D6E63"/><rect y="630" width="800" height="20" fill="#A1887F"/>'
    b += '<ellipse cx="400" cy="640" rx="260" ry="30" fill="#ECEFF1"/>'
    # tiers
    for (y, w, h, c) in ((520, 440, 115, "#FFF8E1"), (410, 330, 110, "#F48FB1"), (315, 220, 95, "#FFF8E1")):
        b += f'<rect x="{400-w/2}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c}"/>'
        b += f'<path d="M{400-w/2} {y+18} ' + " ".join(f'Q{400-w/2+k*40+20} {y+48} {400-w/2+k*40+40} {y+18}' for k in range(int(w/40))) + f' L{400+w/2} {y} L{400-w/2} {y}Z" fill="#8E24AA" opacity=".85"/>'
        b += "".join(f'<circle cx="{400-w/2+30+k*(w-60)/6:.0f}" cy="{y+h*0.65:.0f}" r="7" fill="{cols[k % 5]}"/>' for k in range(7))
    # candles
    for x in (330, 370, 410, 450, 470 - 140):
        pass
    for x in (335, 368, 400, 432, 465):
        b += f'<rect x="{x-7}" y="250" width="14" height="66" rx="4" fill="#4FC3F7"/>'
        b += f'<path d="M{x-7} 262 L{x+7} 256 M{x-7} 282 L{x+7} 276 M{x-7} 302 L{x+7} 296" stroke="#fff" stroke-width="4"/>'
        b += f'<path d="M{x} 212 Q{x+14} 232 {x} 246 Q{x-14} 232 {x} 212Z" fill="#FF9800"/><ellipse cx="{x}" cy="236" rx="4" ry="7" fill="#FFF59D"/>'
    return svg(b, d)


def ferris_wheel():
    d = vgrad("sky", (0, "#1A237E"), (.6, "#7B1FA2"), (1, "#F06292"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    for _ in range(40):
        b += f'<circle cx="{R.randint(0,800)}" cy="{R.randint(0,380)}" r="{R.choice([1.5,2,3])}" fill="#fff" opacity=".8"/>'
    # skyline
    x = 0
    while x < 800:
        w, h = R.randint(40, 90), R.randint(90, 260)
        b += f'<rect x="{x}" y="{700-h}" width="{w}" height="{h+100}" fill="#311B92"/>'
        for wy in range(700 - h + 14, 690, 26):
            for wx in range(x + 8, x + w - 10, 18):
                if R.random() < .45:
                    b += f'<rect x="{wx}" y="{wy}" width="8" height="12" fill="#FFE082" opacity=".85"/>'
        x += w + R.randint(0, 6)
    cx, cy, r = 400, 350, 270
    # legs
    b += f'<path d="M{cx} {cy} L{cx-170} 760 M{cx} {cy} L{cx+170} 760" stroke="#ECEFF1" stroke-width="18" stroke-linecap="round"/>'
    b += f'<path d="M{cx-120} 640 L{cx+120} 640" stroke="#ECEFF1" stroke-width="10"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ECEFF1" stroke-width="12"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="{r-40}" fill="none" stroke="#B0BEC5" stroke-width="5"/>'
    n = 12
    cols = ["#E53935", "#FDD835", "#43A047", "#1E88E5", "#FB8C00", "#EC407A"]
    for i in range(n):
        a = 2 * math.pi * i / n
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        b += f'<line x1="{cx}" y1="{cy}" x2="{px:.0f}" y2="{py:.0f}" stroke="#CFD8DC" stroke-width="5"/>'
    for i in range(n):
        a = 2 * math.pi * i / n
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        b += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="#FFF59D"/>'
        b += f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{px:.0f}" y2="{py+22:.0f}" stroke="#ECEFF1" stroke-width="4"/>'
        b += f'<rect x="{px-26:.0f}" y="{py+20:.0f}" width="52" height="40" rx="10" fill="{cols[i % 6]}"/>'
        b += f'<rect x="{px-17:.0f}" y="{py+27:.0f}" width="34" height="14" rx="4" fill="#FFF8E1"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="30" fill="#ECEFF1"/><circle cx="{cx}" cy="{cy}" r="14" fill="#F06292"/>'
    b += '<rect y="760" width="800" height="40" fill="#1A1040"/>'
    return svg(b, d)


SCENES = {
    "castle": castle, "pirate-ship": pirate_ship, "windmill": windmill, "snowman": snowman,
    "volcano": volcano, "steam-train": steam_train, "octopus": octopus, "pyramids": pyramids,
    "birthday-cake": birthday_cake, "ferris-wheel": ferris_wheel,
}

if __name__ == "__main__":
    for name, fn in SCENES.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(fn())
    print(f"wrote {len(SCENES)} answer images to {os.path.abspath(OUT)}")
