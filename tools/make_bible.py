"""Generates Bible-story answer pictures (800x800 SVG) into ../bible/answers/.
Friendly flat style; each scene uses the story's best-known clue so it is easy to guess.
Run:  python3 tools/make_bible.py
"""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "bible", "answers")
os.makedirs(OUT, exist_ok=True)
R = random.Random(11)

SKIN, SKIN2 = "#E8B98F", "#C98B5E"


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


def arm(sx, sy, ang, length, width, colour, skin=SKIN):
    a = math.radians(ang)
    ex, ey = sx + length * math.cos(a), sy + length * math.sin(a)
    return (f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{colour}" '
            f'stroke-width="{width:.0f}" stroke-linecap="round"/>'
            f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{width*0.42:.0f}" fill="{skin}"/>'), (ex, ey)


def person(cx, base, h, robe, *, skin=SKIN, hair="#5D4037", beard=None, cover=None, cover_band=None,
           arms=(110, 70), sash=None, long_hair=False, stripes=None, smile=True, face=True,
           arm_len=0.36, sleeve=None):
    """Draws a simple robed figure standing on `base`, total height `h`.
    arms = (left_angle, right_angle) in degrees, 90 = straight down, -90 = straight up."""
    s = ""
    sh_y = base - 0.70 * h
    hw_top, hw_bot = 0.15 * h, 0.23 * h
    head_r = 0.105 * h
    head_y = sh_y - head_r * 0.95
    aw, al = 0.075 * h, arm_len * h
    # long hair behind the head
    if long_hair:
        s += f'<path d="M{cx-head_r*1.1:.0f} {head_y-head_r*0.3:.0f} Q{cx-head_r*1.5:.0f} {head_y+head_r*2.8:.0f} {cx-head_r*0.4:.0f} {head_y+head_r*3.2:.0f} L{cx+head_r*0.4:.0f} {head_y+head_r*3.2:.0f} Q{cx+head_r*1.5:.0f} {head_y+head_r*2.8:.0f} {cx+head_r*1.1:.0f} {head_y-head_r*0.3:.0f}Z" fill="{hair}"/>'
    if cover:
        s += f'<path d="M{cx-head_r*1.25:.0f} {head_y-head_r*0.2:.0f} Q{cx:.0f} {head_y-head_r*1.9:.0f} {cx+head_r*1.25:.0f} {head_y-head_r*0.2:.0f} L{cx+head_r*1.45:.0f} {sh_y+0.12*h:.0f} L{cx-head_r*1.45:.0f} {sh_y+0.12*h:.0f}Z" fill="{cover}"/>'
    # feet
    s += f'<ellipse cx="{cx-0.08*h:.0f}" cy="{base:.0f}" rx="{0.06*h:.0f}" ry="{0.025*h:.0f}" fill="#5D4037"/>'
    s += f'<ellipse cx="{cx+0.08*h:.0f}" cy="{base:.0f}" rx="{0.06*h:.0f}" ry="{0.025*h:.0f}" fill="#5D4037"/>'
    # robe
    robe_path = (f'M{cx-hw_top:.0f} {sh_y:.0f} Q{cx:.0f} {sh_y-0.04*h:.0f} {cx+hw_top:.0f} {sh_y:.0f} '
                 f'L{cx+hw_bot:.0f} {base-0.01*h:.0f} Q{cx:.0f} {base+0.02*h:.0f} {cx-hw_bot:.0f} {base-0.01*h:.0f}Z')
    s += f'<path d="{robe_path}" fill="{robe}"/>'
    if stripes:
        clip_id = f"clip{R.randint(0, 10**9)}"
        s += f'<clipPath id="{clip_id}"><path d="{robe_path}"/></clipPath><g clip-path="url(#{clip_id})">'
        n = len(stripes)
        top, bot = sh_y - 0.05 * h, base + 0.03 * h
        for i, c in enumerate(stripes):
            y = top + (bot - top) * i / n
            s += f'<rect x="{cx-hw_bot-5:.0f}" y="{y:.0f}" width="{2*hw_bot+10:.0f}" height="{(bot-top)/n+1:.0f}" fill="{c}"/>'
        s += '</g>'
    if sash:
        s += f'<path d="M{cx-hw_top*1.1:.0f} {sh_y+0.24*h:.0f} L{cx+hw_top*1.1:.0f} {sh_y+0.24*h:.0f}" stroke="{sash}" stroke-width="{0.035*h:.0f}"/>'
    # arms
    la, ra = arms
    sleeve = sleeve or (stripes[1] if stripes else robe)
    a1, _ = arm(cx - hw_top * 0.85, sh_y + 0.04 * h, la, al, aw, sleeve, skin)
    a2, _ = arm(cx + hw_top * 0.85, sh_y + 0.04 * h, ra, al, aw, stripes[-2] if stripes else sleeve, skin)
    s += a1 + a2
    # head
    s += f'<rect x="{cx-0.035*h:.0f}" y="{head_y+head_r*0.6:.0f}" width="{0.07*h:.0f}" height="{0.06*h:.0f}" fill="{skin}"/>'
    s += f'<circle cx="{cx:.0f}" cy="{head_y:.0f}" r="{head_r:.0f}" fill="{skin}"/>'
    if beard:
        s += (f'<path d="M{cx-head_r*0.95:.0f} {head_y+head_r*0.1:.0f} Q{cx-head_r*0.9:.0f} {head_y+head_r*1.9:.0f} {cx:.0f} {head_y+head_r*2.0:.0f} '
              f'Q{cx+head_r*0.9:.0f} {head_y+head_r*1.9:.0f} {cx+head_r*0.95:.0f} {head_y+head_r*0.1:.0f} '
              f'Q{cx:.0f} {head_y+head_r*0.9:.0f} {cx-head_r*0.95:.0f} {head_y+head_r*0.1:.0f}Z" fill="{beard}"/>')
    if cover:
        s += f'<path d="M{cx-head_r*1.2:.0f} {head_y+head_r*0.1:.0f} Q{cx-head_r*1.2:.0f} {head_y-head_r*1.35:.0f} {cx:.0f} {head_y-head_r*1.35:.0f} Q{cx+head_r*1.2:.0f} {head_y-head_r*1.35:.0f} {cx+head_r*1.2:.0f} {head_y+head_r*0.1:.0f} Q{cx:.0f} {head_y-head_r*0.75:.0f} {cx-head_r*1.2:.0f} {head_y+head_r*0.1:.0f}Z" fill="{cover}"/>'
        if cover_band:
            s += f'<path d="M{cx-head_r*1.05:.0f} {head_y-head_r*0.55:.0f} Q{cx:.0f} {head_y-head_r*1.0:.0f} {cx+head_r*1.05:.0f} {head_y-head_r*0.55:.0f}" stroke="{cover_band}" stroke-width="{head_r*0.25:.0f}" fill="none"/>'
    elif hair:
        s += f'<path d="M{cx-head_r*1.02:.0f} {head_y:.0f} Q{cx-head_r:.0f} {head_y-head_r*1.25:.0f} {cx:.0f} {head_y-head_r*1.1:.0f} Q{cx+head_r:.0f} {head_y-head_r*1.25:.0f} {cx+head_r*1.02:.0f} {head_y:.0f} Q{cx+head_r*0.5:.0f} {head_y-head_r*0.6:.0f} {cx:.0f} {head_y-head_r*0.55:.0f} Q{cx-head_r*0.5:.0f} {head_y-head_r*0.6:.0f} {cx-head_r*1.02:.0f} {head_y:.0f}Z" fill="{hair}"/>'
    if face:
        s += f'<circle cx="{cx-head_r*0.36:.0f}" cy="{head_y-head_r*0.05:.0f}" r="{max(2,head_r*0.12):.1f}" fill="#2B1B12"/>'
        s += f'<circle cx="{cx+head_r*0.36:.0f}" cy="{head_y-head_r*0.05:.0f}" r="{max(2,head_r*0.12):.1f}" fill="#2B1B12"/>'
        if smile and not beard:
            s += f'<path d="M{cx-head_r*0.35:.0f} {head_y+head_r*0.38:.0f} Q{cx:.0f} {head_y+head_r*0.68:.0f} {cx+head_r*0.35:.0f} {head_y+head_r*0.38:.0f}" stroke="#8D4E36" stroke-width="{max(2,head_r*0.1):.1f}" fill="none" stroke-linecap="round"/>'
        elif smile:
            s += f'<path d="M{cx-head_r*0.3:.0f} {head_y+head_r*0.5:.0f} Q{cx:.0f} {head_y+head_r*0.72:.0f} {cx+head_r*0.3:.0f} {head_y+head_r*0.5:.0f}" stroke="#8D4E36" stroke-width="{max(2,head_r*0.1):.1f}" fill="none" stroke-linecap="round"/>'
        s += f'<circle cx="{cx-head_r*0.6:.0f}" cy="{head_y+head_r*0.3:.0f}" r="{head_r*0.14:.1f}" fill="#F48FB1" opacity=".5"/>'
        s += f'<circle cx="{cx+head_r*0.6:.0f}" cy="{head_y+head_r*0.3:.0f}" r="{head_r*0.14:.1f}" fill="#F48FB1" opacity=".5"/>'
    return s


def hand_pos(cx, base, h, side, ang, arm_len=0.36):
    hw_top = 0.15 * h
    sx = cx - hw_top * 0.85 if side == "L" else cx + hw_top * 0.85
    sy = base - 0.70 * h + 0.04 * h
    a = math.radians(ang)
    return sx + arm_len * h * math.cos(a), sy + arm_len * h * math.sin(a)


def waves(y, col, n=8, amp=16, w=110, sw=6):
    s = f'<g stroke="{col}" stroke-width="{sw}" fill="none" stroke-linecap="round">'
    for x in range(-40, 840, w):
        s += f'<path d="M{x} {y} q{w/4} {-amp} {w/2} 0 q{w/4} {amp} {w/2} 0"/>'
    return s + '</g>'


def lion(x, y, s=1.0, flip=False):
    f = -1 if flip else 1
    g = f'<g transform="translate({x} {y}) scale({s*f} {s})">'
    g += '<ellipse cx="0" cy="0" rx="90" ry="50" fill="#F9A825"/>'
    g += '<path d="M80 -10 Q130 -40 120 20" stroke="#F9A825" stroke-width="10" fill="none"/><circle cx="120" cy="22" r="10" fill="#8D5524"/>'
    for lx in (-60, -25, 30, 65):
        g += f'<rect x="{lx-9}" y="20" width="18" height="50" rx="8" fill="#F9A825"/>'
    g += '<circle cx="-90" cy="-35" r="58" fill="#A0522D"/>'
    g += '<circle cx="-90" cy="-35" r="38" fill="#FBC02D"/>'
    g += '<circle cx="-104" cy="-44" r="5" fill="#3E2723"/><circle cx="-78" cy="-44" r="5" fill="#3E2723"/>'
    g += '<path d="M-98 -28 L-82 -28 L-90 -20Z" fill="#5D4037"/>'
    g += '<path d="M-100 -14 Q-90 -6 -80 -14" stroke="#5D4037" stroke-width="3" fill="none"/>'
    return g + '</g>'


def sheep(x, y, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    for dx, dy in ((-25, 0), (0, -12), (25, 0), (-12, 12), (12, 12), (0, 5)):
        g += f'<circle cx="{dx}" cy="{dy}" r="22" fill="#FAFAFA" stroke="#E0E0E0" stroke-width="2"/>'
    g += '<ellipse cx="-48" cy="-4" rx="15" ry="18" fill="#424242"/><circle cx="-52" cy="-8" r="3" fill="#fff"/>'
    g += '<rect x="-22" y="26" width="7" height="20" fill="#424242"/><rect x="15" y="26" width="7" height="20" fill="#424242"/>'
    return g + '</g>'


# ---------------------------------------------------------------- scenes

def noahs_ark():
    d = vgrad("sky", (0, "#81D4FA"), (1, "#E1F5FE")) + vgrad("sea", (0, "#1E88E5"), (1, "#0D47A1"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    for i, c in enumerate(["#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#5E35B1"]):
        r = 380 - i * 22
        b += f'<path d="M{400-r} 520 A{r} {r} 0 0 1 {400+r} 520" stroke="{c}" stroke-width="22" fill="none" opacity=".85"/>'
    b += cloud(120, 110) + cloud(680, 150, .8)
    b += '<rect y="560" width="800" height="240" fill="url(#sea)"/>'
    # ark hull
    b += '<path d="M60 470 L740 470 L680 640 Q400 680 120 640Z" fill="#8D6E63"/>'
    b += "".join(f'<line x1="{80+i*6}" y1="{500+i*34}" x2="{720-i*6}" y2="{500+i*34}" stroke="#6D4C41" stroke-width="5"/>' for i in range(4))
    # cabin
    b += '<rect x="200" y="360" width="400" height="115" fill="#A1887F"/>'
    b += '<path d="M180 365 L400 280 L620 365Z" fill="#6D4C41"/>'
    for wx in (240, 360, 480):
        b += f'<rect x="{wx}" y="390" width="80" height="60" rx="6" fill="#3E2723"/>'
    # giraffe in window 1 (neck up through roof line)
    b += '<rect x="262" y="250" width="22" height="200" fill="#FBC02D"/>'
    b += '<ellipse cx="282" cy="245" rx="36" ry="20" fill="#FBC02D"/><circle cx="296" cy="240" r="4" fill="#3E2723"/>'
    b += '<line x1="268" y1="228" x2="262" y2="210" stroke="#8D6E63" stroke-width="5"/><line x1="280" y1="226" x2="280" y2="208" stroke="#8D6E63" stroke-width="5"/>'
    b += "".join(f'<circle cx="{270+(i%2)*10}" cy="{270+i*28}" r="5" fill="#A1662F"/>' for i in range(6))
    # elephant in window 2
    b += '<circle cx="400" cy="420" r="30" fill="#90A4AE"/><ellipse cx="372" cy="418" rx="16" ry="22" fill="#78909C"/><ellipse cx="428" cy="418" rx="16" ry="22" fill="#78909C"/>'
    b += '<path d="M400 430 Q402 460 388 466" stroke="#90A4AE" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="390" cy="412" r="3.5" fill="#263238"/><circle cx="410" cy="412" r="3.5" fill="#263238"/>'
    # lion head in window 3
    b += '<circle cx="520" cy="420" r="30" fill="#A0522D"/><circle cx="520" cy="420" r="19" fill="#FBC02D"/><circle cx="513" cy="415" r="3" fill="#3E2723"/><circle cx="527" cy="415" r="3" fill="#3E2723"/>'
    # Noah on the deck
    b += person(660, 470, 190, "#8D6E63", beard="#ECEFF1", hair="#ECEFF1", arms=(-130, -50), sash="#FFCA28")
    # dove with olive branch
    b += '<g transform="translate(560 170)"><ellipse rx="34" ry="18" fill="#fff"/><path d="M-5 -5 Q-30 -45 -55 -30 Q-30 -15 -5 5Z" fill="#fff" stroke="#CFD8DC" stroke-width="2"/>'
    b += '<circle cx="30" cy="-8" r="13" fill="#fff"/><path d="M42 -8 L54 -4 L42 0Z" fill="#FFA000"/><circle cx="33" cy="-11" r="2.5" fill="#263238"/>'
    b += '<path d="M50 -2 Q70 10 84 8" stroke="#558B2F" stroke-width="3" fill="none"/><ellipse cx="66" cy="8" rx="7" ry="3.5" fill="#7CB342"/><ellipse cx="78" cy="4" rx="7" ry="3.5" fill="#7CB342"/></g>'
    b += waves(700, "#90CAF9") + waves(760, "#64B5F6")
    return svg(b, d)


def david_goliath():
    d = vgrad("sky", (0, "#90CAF9"), (1, "#FFF8E1"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>' + cloud(160, 110, .8)
    b += '<path d="M0 600 Q200 520 420 590 T800 560 L800 800 L0 800Z" fill="#AED581"/>'
    b += '<path d="M0 700 Q400 640 800 700 L800 800 L0 800Z" fill="#8BC34A"/>'
    # Goliath (huge) on the right
    gx, gbase, gh = 560, 760, 700
    b += person(gx, gbase, gh, "#5D4037", beard="#3E2723", hair="#3E2723", arms=(120, 60), smile=False)
    # armour chest plate + helmet
    sh_y = gbase - 0.70 * gh
    b += f'<path d="M{gx-95} {sh_y+10} L{gx+95} {sh_y+10} L{gx+80} {sh_y+190} L{gx-80} {sh_y+190}Z" fill="#9E9E9E" stroke="#616161" stroke-width="5"/>'
    b += "".join(f'<line x1="{gx-85}" y1="{sh_y+40+i*35}" x2="{gx+85}" y2="{sh_y+40+i*35}" stroke="#757575" stroke-width="4"/>' for i in range(4))
    hy = sh_y - 0.105 * gh * 0.95
    b += f'<path d="M{gx-82} {hy-5} Q{gx} {hy-120} {gx+82} {hy-5} L{gx+82} {hy+10} L{gx-82} {hy+10}Z" fill="#B0BEC5" stroke="#607D8B" stroke-width="5"/>'
    b += f'<path d="M{gx-8} {hy-95} Q{gx} {hy-150} {gx+30} {hy-140} Q{gx+10} {hy-110} {gx+8} {hy-95}Z" fill="#C62828"/>'
    # angry eyebrows
    b += f'<path d="M{gx-40} {hy-10} L{gx-14} {hy+2} M{gx+40} {hy-10} L{gx+14} {hy+2}" stroke="#3E2723" stroke-width="7" stroke-linecap="round"/>'
    # spear + shield
    hx, hy2 = hand_pos(gx, gbase, gh, "R", 60)
    b += f'<line x1="{hx+10}" y1="{hy2+200}" x2="{hx-20}" y2="{hy2-420}" stroke="#6D4C41" stroke-width="14"/>'
    b += f'<path d="M{hx-35} {hy2-420} L{hx-20} {hy2-490} L{hx-5} {hy2-420}Z" fill="#B0BEC5"/>'
    lx, ly = hand_pos(gx, gbase, gh, "L", 120)
    b += f'<circle cx="{lx}" cy="{ly}" r="85" fill="#FFB300" stroke="#8D6E63" stroke-width="8"/><circle cx="{lx}" cy="{ly}" r="20" fill="#8D6E63"/>'
    # David (small) on the left with a sling
    dx, dbase, dh = 170, 720, 240
    b += person(dx, dbase, dh, "#43A047", hair="#6D4C41", arms=(100, -60), sash="#8D6E63")
    sx, sy = hand_pos(dx, dbase, dh, "R", -60)
    b += f'<path d="M{sx} {sy} Q{sx+30} {sy-80} {sx-10} {sy-110}" stroke="#795548" stroke-width="4" fill="none"/>'
    b += f'<circle cx="{sx-10}" cy="{sy-112}" r="12" fill="#9E9E9E"/>'
    b += f'<path d="M{sx+40} {sy-150} A70 70 0 0 1 {sx+70} {sy-60}" stroke="#fff" stroke-width="5" fill="none" stroke-dasharray="10 10" opacity=".9"/>'
    # stones on ground + a sheep
    for x in (90, 115, 140):
        b += f'<ellipse cx="{x}" cy="745" rx="12" ry="8" fill="#9E9E9E"/>'
    b += sheep(80, 610, .8)
    return svg(b, d)


def moses_red_sea():
    d = vgrad("sky", (0, "#FFB74D"), (1, "#FFE0B2")) + vgrad("wall", (0, "#0D47A1"), (1, "#42A5F5"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="400" cy="150" r="70" fill="#FFF3E0"/>'
    b += '<path d="M280 800 L360 300 L440 300 L520 800Z" fill="#E6B775"/>'
    # water walls with waves on top
    b += '<path d="M0 180 Q80 150 150 190 Q220 230 300 200 L350 300 L270 800 L0 800Z" fill="url(#wall)"/>'
    b += '<path d="M800 180 Q720 150 650 190 Q580 230 500 200 L450 300 L530 800 L800 800Z" fill="url(#wall)"/>'
    b += '<g stroke="#BBDEFB" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8">'
    for y in range(260, 760, 70):
        b += f'<path d="M20 {y} q40 -20 80 0 q40 20 80 0"/><path d="M620 {y+30} q40 -20 80 0 q40 20 80 0"/>'
    b += '</g>'
    b += '<g fill="#fff">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((300, 200, 14), (320, 225, 9), (500, 200, 14), (480, 225, 9), (150, 190, 10), (650, 190, 10))) + '</g>'
    # fish in the wall
    b += '<g transform="translate(120 480)"><ellipse rx="26" ry="14" fill="#FFB300"/><path d="M24 0 L44 -14 L44 14Z" fill="#FFB300"/><circle cx="-12" cy="-3" r="3" fill="#212121"/></g>'
    b += '<g transform="translate(690 560) scale(-1 1)"><ellipse rx="26" ry="14" fill="#F06292"/><path d="M24 0 L44 -14 L44 14Z" fill="#F06292"/><circle cx="-12" cy="-3" r="3" fill="#212121"/></g>'
    # people following, small, far back
    for x, c in ((375, "#7E57C2"), (400, "#26A69A"), (425, "#EF5350")):
        b += person(x, 380, 70, c, hair="#4E342E", face=False)
    # Moses with staff raised
    mx, mbase, mh = 400, 760, 330
    b += person(mx, mbase, mh, "#C62828", beard="#ECEFF1", hair="#ECEFF1", arms=(100, -70), sash="#FFCA28", cover="#FFF3E0", cover_band="#8D6E63")
    hx, hy = hand_pos(mx, mbase, mh, "R", -70)
    b += f'<line x1="{hx-20}" y1="{hy+160}" x2="{hx+25}" y2="{hy-150}" stroke="#6D4C41" stroke-width="12" stroke-linecap="round"/>'
    b += f'<path d="M{hx+25} {hy-150} q20 -10 18 -30" stroke="#6D4C41" stroke-width="12" fill="none" stroke-linecap="round"/>'
    b += f'<circle cx="{hx+30}" cy="{hy-160}" r="40" fill="#FFF59D" opacity=".45"/>'
    return svg(b, d)


def jonah():
    d = vgrad("sea", (0, "#29B6F6"), (1, "#01579B"))
    b = '<rect width="800" height="800" fill="url(#sea)"/>'
    for x in range(-100, 900, 110):
        b += f'<path d="M{x} 0 L{x+40} 0 L{x+180} 800 L{x+140} 800Z" fill="#fff" opacity=".05"/>'
    b += '<rect width="800" height="90" fill="#B3E5FC"/>' + waves(90, "#fff", sw=5)
    # big fish body across the board
    b += '<path d="M60 430 Q120 190 420 210 Q640 225 700 380 L790 280 L770 430 L790 580 L700 480 Q640 640 400 650 Q120 650 60 430Z" fill="#5C6BC0"/>'
    b += '<path d="M120 500 Q300 620 560 560 Q640 540 690 470 Q620 610 400 640 Q180 630 120 500Z" fill="#9FA8DA"/>'
    b += '<path d="M380 215 Q430 130 520 150 Q470 190 470 225Z" fill="#3949AB"/>'
    # open mouth with Jonah inside
    b += '<path d="M60 430 L260 360 L260 500Z" fill="#311B92"/>'
    b += '<path d="M60 430 L260 360" stroke="#FAFAFA" stroke-width="6" stroke-dasharray="14 8"/><path d="M60 430 L260 500" stroke="#FAFAFA" stroke-width="6" stroke-dasharray="14 8"/>'
    b += person(185, 480, 130, "#FFB300", hair="#4E342E", beard="#4E342E", arms=(-140, -40), sash="#6D4C41")
    # eye + water spout
    b += '<circle cx="300" cy="320" r="26" fill="#fff"/><circle cx="292" cy="322" r="13" fill="#1A1A2E"/><circle cx="288" cy="316" r="4" fill="#fff"/>'
    b += '<path d="M430 210 Q420 120 380 90 M430 210 Q440 110 480 80 M430 210 L430 80" stroke="#E1F5FE" stroke-width="10" fill="none" stroke-linecap="round"/>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#E1F5FE" stroke-width="3"/>' for x, y, r in ((90, 300, 12), (110, 260, 8), (740, 650, 14), (700, 700, 9), (560, 710, 11)))
    # small boat far away
    b += '<path d="M600 70 L700 70 L685 90 L615 90Z" fill="#6D4C41"/><path d="M648 70 L648 20 L690 66Z" fill="#FFF8E1"/>'
    b += '<path d="M0 760 Q200 720 400 760 T800 750 L800 800 L0 800Z" fill="#FFE082"/>'
    return svg(b, d)


def daniel_lions():
    d = vgrad("den", (0, "#5D4037"), (1, "#3E2723"))
    b = '<rect width="800" height="800" fill="url(#den)"/>'
    for row in range(8):
        for col in range(7):
            x = col * 120 + (row % 2) * 60 - 40
            b += f'<rect x="{x}" y="{row*70}" width="112" height="62" rx="8" fill="#6D4C41" opacity=".6"/>'
    # light from opening above
    b += '<path d="M330 0 L470 0 L620 800 L180 800Z" fill="#FFF59D" opacity=".18"/>'
    b += '<rect y="620" width="800" height="180" fill="#8D6E63"/>'
    b += lion(160, 640, 1.05) + lion(640, 640, 1.05, flip=True) + lion(400, 740, 0.8)
    # Daniel praying (hands together)
    b += person(400, 600, 330, "#1565C0", hair="#4E342E", beard="#4E342E", arms=(50, 130), sash="#FFCA28",
                cover="#FFF8E1", cover_band="#0D47A1", arm_len=0.2, sleeve="#0D47A1")
    lx, ly = hand_pos(400, 600, 330, "L", 50, 0.2)
    b += f'<path d="M400 {ly-45:.0f} Q388 {ly-10:.0f} 384 {ly+8:.0f} L416 {ly+8:.0f} Q412 {ly-10:.0f} 400 {ly-45:.0f}Z" fill="{SKIN}" stroke="#C98B5E" stroke-width="2"/>'
    # angel glow
    b += '<circle cx="400" cy="250" r="190" fill="#FFF9C4" opacity=".12"/>'
    return svg(b, d)


def adam_eve():
    d = vgrad("sky", (0, "#B2EBF2"), (1, "#E8F5E9"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    b += '<path d="M0 560 Q200 500 400 540 T800 520 L800 800 L0 800Z" fill="#81C784"/>'
    b += '<path d="M0 660 Q400 600 800 660 L800 800 L0 800Z" fill="#66BB6A"/>'
    for x, y, c in ((60, 700, "#EC407A"), (120, 740, "#FFEB3B"), (700, 720, "#AB47BC"), (760, 690, "#FF7043"), (340, 760, "#FFEB3B"), (480, 770, "#EC407A")):
        b += f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/><circle cx="{x}" cy="{y}" r="3.5" fill="#FFF59D"/>'
    # the tree
    b += '<path d="M360 700 Q370 520 340 430 L460 430 Q430 520 440 700Z" fill="#6D4C41"/>'
    for x, y, r in ((400, 230, 170), (250, 320, 120), (550, 320, 120), (320, 180, 110), (480, 180, 110), (400, 380, 120)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#2E7D32"/>'
    for x, y, r in ((360, 170, 60), (470, 260, 50)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#43A047"/>'
    for x, y in ((280, 280), (360, 330), (450, 300), (520, 360), (330, 200), (470, 170), (400, 250), (560, 260), (240, 360)):
        b += f'<circle cx="{x}" cy="{y}" r="16" fill="#E53935"/><path d="M{x} {y-15} l4 -8" stroke="#5D4037" stroke-width="3"/>'
    # serpent on the trunk
    b += '<path d="M330 640 Q460 600 350 560 Q250 520 420 480 Q520 450 440 420" stroke="#7CB342" stroke-width="24" fill="none" stroke-linecap="round"/>'
    b += '<ellipse cx="445" cy="410" rx="26" ry="18" fill="#7CB342"/><circle cx="452" cy="404" r="4" fill="#212121"/>'
    b += '<path d="M468 414 L488 410 M488 410 l6 -5 M488 410 l6 5" stroke="#E53935" stroke-width="3" fill="none"/>'
    # Adam and Eve in leaf clothing
    b += person(170, 740, 300, "#558B2F", hair="#5D4037", arms=(100, 40))
    b += person(630, 740, 290, "#689F38", hair="#8D4E36", long_hair=True, arms=(140, 70))
    ex, ey = hand_pos(630, 740, 290, "L", 140)
    b += f'<circle cx="{ex}" cy="{ey-8}" r="20" fill="#E53935"/><path d="M{ex} {ey-28} l4 -10" stroke="#5D4037" stroke-width="3"/>'
    for cx, base, h in ((170, 740, 300), (630, 740, 290)):
        for k in range(5):
            yy = base - 0.70 * h + 30 + k * 36
            b += f'<ellipse cx="{cx-40+(k%2)*80}" cy="{yy:.0f}" rx="24" ry="10" fill="#33691E" opacity=".6" transform="rotate({(-1)**k*25} {cx-40+(k%2)*80} {yy:.0f})"/>'
    b += '<g transform="translate(720 620)"><ellipse rx="26" ry="20" fill="#fff"/><ellipse cx="-8" cy="-30" rx="6" ry="18" fill="#fff"/><ellipse cx="6" cy="-30" rx="6" ry="18" fill="#fff"/><circle cx="-6" cy="-6" r="3" fill="#212121"/></g>'
    return svg(b, d)


def nativity():
    d = vgrad("sky", (0, "#0D1B3E"), (1, "#283593"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    for _ in range(50):
        b += f'<circle cx="{R.randint(0,800)}" cy="{R.randint(0,330)}" r="{R.choice([1.5,2,2.5])}" fill="#fff" opacity=".8"/>'
    # the star
    b += '<g transform="translate(400 90)">'
    b += '<path d="M0 -60 L14 -14 L60 0 L14 14 L0 60 L-14 14 L-60 0 L-14 -14Z" fill="#FFF59D"/>'
    b += '<path d="M0 -30 L8 -8 L30 0 L8 8 L0 30 L-8 8 L-30 0 L-8 -8Z" fill="#fff" transform="rotate(45)"/></g>'
    b += '<path d="M400 120 L300 470 L500 470Z" fill="#FFF59D" opacity=".15"/>'
    # stable
    b += '<rect y="690" width="800" height="110" fill="#5D4037"/>'
    b += '<rect x="90" y="330" width="620" height="370" fill="#795548"/>'
    b += "".join(f'<rect x="{x}" y="330" width="6" height="370" fill="#6D4C41"/>' for x in range(120, 700, 70))
    b += '<path d="M50 350 L400 180 L750 350 L720 370 L400 215 L80 370Z" fill="#4E342E"/>'
    b += '<rect x="90" y="600" width="620" height="100" fill="#FBC02D" opacity=".35"/>'
    # manger with baby
    b += '<path d="M290 600 L510 600 L480 670 L320 670Z" fill="#8D6E63"/><path d="M300 690 L330 640 M500 690 L470 640" stroke="#5D4037" stroke-width="10"/>'
    b += '<path d="M290 600 Q400 570 510 600" stroke="#FDD835" stroke-width="16" fill="none"/>'
    b += '<circle cx="400" cy="555" r="48" fill="#FFF59D" opacity=".6"/>'
    b += '<ellipse cx="410" cy="585" rx="65" ry="28" fill="#FFF8E1"/><path d="M370 580 Q410 570 460 588" stroke="#E0D6C2" stroke-width="3" fill="none"/>'
    b += f'<circle cx="350" cy="575" r="24" fill="{SKIN}"/><path d="M340 574 q4 4 8 0 M352 574 q4 4 8 0" stroke="#2B1B12" stroke-width="2.5" fill="none"/>'
    b += '<circle cx="350" cy="575" r="34" fill="none" stroke="#FFE082" stroke-width="5"/>'
    # Mary and Joseph
    b += person(210, 690, 300, "#1E88E5", hair="#4E342E", cover="#90CAF9", arms=(60, 40))
    b += person(590, 690, 320, "#8D6E63", beard="#4E342E", hair="#4E342E", cover="#D7CCC8", cover_band="#6D4C41", arms=(110, -80))
    hx, hy = hand_pos(590, 690, 320, "R", -80)
    b += f'<line x1="{hx}" y1="{hy-60}" x2="{hx+10}" y2="{hy+260}" stroke="#5D4037" stroke-width="10" stroke-linecap="round"/><path d="M{hx} {hy-60} q-5 -30 -30 -25" stroke="#5D4037" stroke-width="10" fill="none" stroke-linecap="round"/>'
    b += sheep(110, 730, .85) + sheep(700, 735, .8)
    # donkey head peeking
    b += '<g transform="translate(700 470)"><ellipse rx="34" ry="48" fill="#9E9E9E"/><ellipse cx="-16" cy="-50" rx="9" ry="28" fill="#9E9E9E"/><ellipse cx="16" cy="-50" rx="9" ry="28" fill="#9E9E9E"/><ellipse cy="30" rx="26" ry="18" fill="#BDBDBD"/><circle cx="-12" cy="-8" r="4" fill="#212121"/><circle cx="12" cy="-8" r="4" fill="#212121"/></g>'
    return svg(b, d)


def josephs_coat():
    d = vgrad("sky", (0, "#FFE082"), (1, "#FFF8E1"))
    b = '<rect width="800" height="800" fill="url(#sky)"/><circle cx="660" cy="130" r="60" fill="#FFF3E0"/>'
    b += '<path d="M0 560 Q250 500 500 550 T800 530 L800 800 L0 800Z" fill="#E6B775"/>'
    b += '<path d="M0 660 Q400 610 800 670 L800 800 L0 800Z" fill="#D7A15A"/>'
    # palm + tents
    b += '<path d="M90 580 L150 480 L210 580Z" fill="#8D6E63"/><path d="M630 560 L700 450 L770 560Z" fill="#A1887F"/>'
    # Joseph, big, arms out to show off the coat
    stripes = ["#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA", "#EC407A", "#00ACC1", "#7CB342"]
    b += person(400, 760, 600, "#E53935", hair="#4E342E", arms=(160, 20), stripes=stripes)
    # brothers, small and grumpy in the distance
    for x, c in ((110, "#8D6E63"), (170, "#6D4C41"), (660, "#795548"), (720, "#8D6E63")):
        b += person(x, 640, 110, c, hair="#3E2723", beard="#3E2723", smile=False)
    b += sheep(110, 720, .7) + sheep(700, 730, .75)
    return svg(b, d)


def samson():
    d = vgrad("sky", (0, "#4E342E"), (1, "#8D6E63"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>'
    b += '<rect y="700" width="800" height="100" fill="#5D4037"/>'
    # temple roof block cracking
    b += '<rect x="0" y="60" width="800" height="110" fill="#BCAAA4"/><path d="M0 170 L800 170" stroke="#8D6E63" stroke-width="8"/>'
    b += '<path d="M380 60 L400 110 L385 140 L410 170" stroke="#3E2723" stroke-width="6" fill="none"/>'
    b += '<path d="M150 60 L170 100 L160 130" stroke="#3E2723" stroke-width="5" fill="none"/><path d="M640 60 L620 110 L640 150" stroke="#3E2723" stroke-width="5" fill="none"/>'
    # falling stones
    for x, y, r in ((300, 220, 14), (520, 250, 18), (240, 320, 10), (580, 330, 12), (430, 200, 9)):
        b += f'<rect x="{x}" y="{y}" width="{r*2}" height="{r*1.6:.0f}" rx="3" fill="#A1887F" transform="rotate({R.randint(-30,30)} {x} {y})"/>'
    # two pillars being pushed apart (tilted)
    b += '<g transform="rotate(-6 150 700)"><rect x="90" y="170" width="120" height="530" fill="#D7CCC8"/>'
    b += "".join(f'<line x1="{x}" y1="170" x2="{x}" y2="700" stroke="#BCAAA4" stroke-width="6"/>' for x in (120, 150, 180))
    b += '<rect x="75" y="160" width="150" height="30" fill="#EFEBE9"/><rect x="75" y="690" width="150" height="30" fill="#EFEBE9"/></g>'
    b += '<g transform="rotate(6 650 700)"><rect x="590" y="170" width="120" height="530" fill="#D7CCC8"/>'
    b += "".join(f'<line x1="{x}" y1="170" x2="{x}" y2="700" stroke="#BCAAA4" stroke-width="6"/>' for x in (620, 650, 680))
    b += '<rect x="575" y="160" width="150" height="30" fill="#EFEBE9"/><rect x="575" y="690" width="150" height="30" fill="#EFEBE9"/></g>'
    # Samson: strong, very long hair, arms out pushing
    b += person(400, 720, 470, "#E65100", skin=SKIN2, hair="#2B1B12", long_hair=True, beard="#2B1B12", arms=(185, -5), sash="#FFCA28")
    # muscles
    for x in (290, 510):
        b += f'<ellipse cx="{x}" cy="{720-0.70*470+30:.0f}" rx="30" ry="22" fill="{SKIN2}"/>'
    # effort lines
    b += '<g stroke="#FFF59D" stroke-width="6" stroke-linecap="round">' + "".join(f'<line x1="{x}" y1="{y}" x2="{x+dx}" y2="{y+dy}"/>' for x, y, dx, dy in ((230, 360, -30, -20), (230, 400, -35, 0), (570, 360, 30, -20), (570, 400, 35, 0))) + '</g>'
    return svg(b, d)


def zacchaeus():
    d = vgrad("sky", (0, "#81D4FA"), (1, "#E1F5FE"))
    b = '<rect width="800" height="800" fill="url(#sky)"/>' + cloud(130, 100, .8)
    b += '<rect y="640" width="800" height="160" fill="#D7B377"/>'
    # houses of Jericho
    b += '<rect x="610" y="450" width="190" height="200" fill="#F5DEB3"/><rect x="650" y="500" width="40" height="50" fill="#8D6E63"/><rect x="720" y="580" width="45" height="70" fill="#6D4C41"/>'
    # big sycamore tree
    b += '<path d="M180 660 Q200 470 170 360 L260 360 Q240 470 270 660Z" fill="#6D4C41"/>'
    b += '<path d="M215 400 Q330 330 480 330" stroke="#6D4C41" stroke-width="30" fill="none" stroke-linecap="round"/>'
    for x, y, r in ((220, 200, 170), (380, 180, 140), (520, 250, 110), (90, 290, 110), (300, 300, 120)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#388E3C"/>'
    for x, y, r in ((200, 140, 60), (390, 140, 50), (520, 220, 40)):
        b += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#4CAF50"/>'
    # Zacchaeus on the branch, small, peering down
    b += person(420, 332, 150, "#7B1FA2", hair="#4E342E", beard="#4E342E", arms=(40, -150), sash="#FFCA28")
    # crowd below
    for x, c, h in ((470, "#EF5350", 170), (540, "#26A69A", 180), (610, "#FFA726", 165)):
        b += person(x, 760, h, c, hair="#3E2723", face=False)
    # Jesus looking up and waving
    b += person(330, 770, 290, "#FAFAFA", hair="#5D4037", beard="#5D4037", arms=(100, -60), sash="#C62828", long_hair=True)
    return svg(b, d)


SCENES = {
    "noahs-ark": (noahs_ark, "Noah's Ark"),
    "david-and-goliath": (david_goliath, "David and Goliath"),
    "moses-red-sea": (moses_red_sea, "Moses parts the Red Sea"),
    "jonah-big-fish": (jonah, "Jonah and the big fish"),
    "daniel-lions-den": (daniel_lions, "Daniel in the lions' den"),
    "adam-and-eve": (adam_eve, "Adam and Eve"),
    "baby-jesus-manger": (nativity, "Baby Jesus in the manger"),
    "josephs-coat": (josephs_coat, "Joseph's coat of many colours"),
    "samson": (samson, "Samson"),
    "zacchaeus": (zacchaeus, "Zacchaeus in the tree"),
}

if __name__ == "__main__":
    for name, (fn, _) in SCENES.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as f:
            f.write(fn())
    print(f"wrote {len(SCENES)} Bible pictures to {os.path.abspath(OUT)}")
