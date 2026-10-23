import cairo, math, random, sys, subprocess

W, H, FPS, DUR = 1080, 1920, 30, 20.0
N = int(FPS * DUR)
S = [0.0, 2.4, 4.8, 9.4, 12.6, 15.6, 18.0, 20.0]   # scene boundaries
TR = 0.16                                          # half transition length

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

C = dict(navy='#0b1640', navy2='#1c2d72', purple='#35237e', pink='#ff4f81', cyan='#3ee0ff',
         yellow='#ffd23f', orange='#ff8a3d', green='#5ee38a', red='#ff4757', white='#ffffff',
         skin='#ffc9a0', grey='#9aaad6', steel='#6b7fb8', dark='#08102e', hair='#2b1d4f',
         pants='#26357a', ocean='#2d6be0', land='#45c486')

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def ss(x): x = clamp(x); return x * x * (3 - 2 * x)
def eback(x, s=2.0):
    x = clamp(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x

def src(ctx, col, a=1.0):
    r, g, b, aa = hexc(col) if isinstance(col, str) else col
    ctx.set_source_rgba(r, g, b, aa * a)

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()

def circle(ctx, x, y, r, col, a=1.0):
    ctx.arc(x, y, r, 0, 2 * math.pi); src(ctx, col, a); ctx.fill()

def glow(ctx, x, y, r, col, a=0.5):
    cr, cg, cb, _ = hexc(col)
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, cr, cg, cb, a)
    g.add_color_stop_rgba(0.4, cr, cg, cb, a * 0.35)
    g.add_color_stop_rgba(1, cr, cg, cb, 0)
    ctx.set_source(g); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.fill()

# ---------------------------------------------------------------- background
random.seed(7)
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1.2, 3.6), random.uniform(0, 6.28),
          random.uniform(0.6, 2.2)) for _ in range(140)]

def bg(ctx, t, top=C['navy'], bot=C['navy2'], glow_col=C['purple'], gx=540, gy=1100, drift=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hexc(top)); g.add_color_stop_rgba(1, *hexc(bot))
    ctx.set_source(g); ctx.paint()
    glow(ctx, gx, gy, 1100, glow_col, 0.55)
    for (x, y, r, ph, sp) in STARS:
        yy = (y - drift * sp) % H
        a = 0.35 + 0.45 * (0.5 + 0.5 * math.sin(t * sp * 2.2 + ph))
        circle(ctx, x, yy, r, C['white'], a)

def vignette(ctx):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 0.75)
    g.add_color_stop_rgba(0, 0, 0, 0.05, 0); g.add_color_stop_rgba(1, 0, 0, 0.05, 0.55)
    ctx.set_source(g); ctx.paint()

# ---------------------------------------------------------------- text
def font(ctx, size, w='bold'):
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if w == 'bold' else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def rich(ctx, parts, x, y, size, p=1.0, maxw=940, w='bold', pop=True, align='center', shadow=True):
    """parts: list of (text, color). y = visual centre line."""
    if p <= 0: return
    if isinstance(parts, str): parts = [(parts, C['white'])]
    font(ctx, size, w)
    total = sum(ctx.text_extents(s).x_advance for s, _ in parts)
    if total > maxw:
        size *= maxw / total; font(ctx, size, w)
        total = sum(ctx.text_extents(s).x_advance for s, _ in parts)
    asc, desc = ctx.font_extents()[0], ctx.font_extents()[1]
    sc = eback(p) if pop else 1.0
    a = clamp(p * 2.5)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc)
    cx = -total / 2 if align == 'center' else 0
    base = size * 0.36
    for s, col in parts:
        adv = ctx.text_extents(s).x_advance
        if shadow:
            ctx.set_source_rgba(0.02, 0.03, 0.12, 0.45 * a); ctx.move_to(cx, base + size * 0.07); ctx.show_text(s)
        src(ctx, col, a); ctx.move_to(cx, base); ctx.show_text(s)
        cx += adv
    ctx.restore()

def source_line(ctx, txt, a=1.0, y=1835):
    rich(ctx, [(txt, C['grey'])], 540, y, 30, p=a, pop=False, w='normal', shadow=False)

# ---------------------------------------------------------------- characters & props
def person(ctx, x, y, s=1.0, shirt=C['orange'], arm_l=0.15, arm_r=0.15, rot=0.0, a=1.0,
           skin=C['skin'], hair=C['hair'], pants=C['pants'], eyes=True, mono=None):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if mono: shirt = skin = hair = pants = mono
    sh = hexc(shirt)
    dark = (sh[0] * 0.78, sh[1] * 0.78, sh[2] * 0.78, 1)
    # shadow ellipse
    ctx.save(); ctx.scale(1, 0.25); circle(ctx, 0, 0, 60, C['dark'], 0.35 * a); ctx.restore()
    for lx in (-27, 3):
        rrect(ctx, lx, -72, 24, 72, 11); src(ctx, pants, a); ctx.fill()
    for side, ang in ((-1, arm_l), (1, arm_r)):
        ctx.save(); ctx.translate(side * 31, -136); ctx.rotate(-side * ang)
        rrect(ctx, -10, -6, 20, 76, 10); src(ctx, dark, a); ctx.fill()
        circle(ctx, 0, 72, 11, skin, a)
        ctx.restore()
    rrect(ctx, -40, -152, 80, 96, 32); src(ctx, shirt, a); ctx.fill()
    rrect(ctx, -40, -152, 80, 30, 15); ctx.set_source_rgba(1, 1, 1, 0.12 * a); ctx.fill()
    circle(ctx, 0, -186, 33, skin, a)
    ctx.arc(0, -190, 34, math.pi * 1.05, math.pi * 1.95); ctx.close_path(); src(ctx, hair, a); ctx.fill()
    if eyes and not mono:
        circle(ctx, -11, -182, 4.2, C['dark'], a); circle(ctx, 11, -182, 4.2, C['dark'], a)
    ctx.restore()

def mini(ctx, x, y, rot, s, col, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -9, -30, 18, 30, 8); src(ctx, col, a); ctx.fill()
    circle(ctx, 0, -40, 9, col, a)
    ctx.restore()

def laptop(ctx, x, y, s=1.0, a=1.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    glow(ctx, 0, -80, 230, C['cyan'], 0.35 * a)
    rrect(ctx, -100, -150, 200, 136, 14); src(ctx, '#27346e', a); ctx.fill()
    g = cairo.LinearGradient(0, -140, 0, -24)
    g.add_color_stop_rgba(0, *hexc(C['cyan'], a)); g.add_color_stop_rgba(1, *hexc('#2aa4e8', a))
    rrect(ctx, -88, -139, 176, 114, 8); ctx.set_source(g); ctx.fill()
    for i in range(5):
        wl = 40 + ((i * 37 + int(t * 8)) % 90)
        rrect(ctx, -72, -125 + i * 20, wl, 8, 4); ctx.set_source_rgba(0.05, 0.1, 0.3, 0.45 * a); ctx.fill()
    rrect(ctx, -118, -16, 236, 18, 9); src(ctx, '#d4dcf2', a); ctx.fill()
    ctx.restore()

def robot_arm(ctx, base, target, L1=720, L2=640, claw=0.5, carry=None, t=0.0):
    bx, by = base; tx, ty = target
    d = math.hypot(tx - bx, ty - by)
    d = clamp(d, abs(L1 - L2) + 5, L1 + L2 - 5)
    a = math.atan2(ty - by, tx - bx)
    b = math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1))
    a1 = a - b
    ex, ey = bx + L1 * math.cos(a1), by + L1 * math.sin(a1)
    a2 = math.atan2(ty - ey, tx - ex)
    wx, wy = ex + L2 * math.cos(a2), ey + L2 * math.sin(a2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for (p0, p1, wdt) in (((bx, by), (ex, ey), 78), ((ex, ey), (wx, wy), 60)):
        ctx.move_to(*p0); ctx.line_to(*p1); ctx.set_line_width(wdt); src(ctx, C['steel']); ctx.stroke()
        ctx.move_to(p0[0] - 12, p0[1] - 8); ctx.line_to(p1[0] - 12, p1[1] - 8)
        ctx.set_line_width(wdt * 0.25); ctx.set_source_rgba(1, 1, 1, 0.22); ctx.stroke()
    if carry:
        carry(wx, wy)
    for (jx, jy, r) in ((ex, ey, 52), (wx, wy, 44)):
        circle(ctx, jx, jy, r, '#3b4a86'); circle(ctx, jx, jy, r * 0.55, '#56679f')
    # claw fingers
    for side in (-1, 1):
        ang = a2 + side * (0.25 + claw * 0.55)
        fx, fy = wx + 34 * math.cos(ang), wy + 34 * math.sin(ang)
        tx2, ty2 = fx + 70 * math.cos(ang), fy + 70 * math.sin(ang)
        ang2 = a2 - side * 0.5
        tx3, ty3 = tx2 + 40 * math.cos(ang2), ty2 + 40 * math.sin(ang2)
        ctx.move_to(fx, fy); ctx.line_to(tx2, ty2); ctx.line_to(tx3, ty3)
        ctx.set_line_width(24); ctx.set_line_join(cairo.LINE_JOIN_ROUND); src(ctx, '#8597cc'); ctx.stroke()
    pulse = 0.6 + 0.4 * math.sin(t * 12)
    glow(ctx, wx, wy, 70, C['pink'], 0.8 * pulse); circle(ctx, wx, wy, 13, C['pink'])
    return wx, wy

def planet(ctx, cx, cy, r, rot):
    glow(ctx, cx, cy, r * 1.55, C['cyan'], 0.4)
    ctx.save(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    g = cairo.LinearGradient(cx - r, cy - r, cx + r, cy + r)
    g.add_color_stop_rgba(0, *hexc('#4a8cff')); g.add_color_stop_rgba(1, *hexc('#2246b8'))
    ctx.set_source(g); ctx.paint()
    blobs = [(0.0, -0.3, 0.55, 0.35), (1.4, 0.25, 0.45, 0.5), (2.6, -0.55, 0.4, 0.22), (3.7, 0.35, 0.6, 0.3),
             (4.9, -0.1, 0.35, 0.45), (5.6, 0.6, 0.3, 0.18), (2.1, 0.75, 0.5, 0.15), (0.8, 0.55, 0.25, 0.2)]
    for lon, lat, rx, ry in blobs:
        L = lon + rot
        c = math.cos(L)
        if c < -0.15: continue
        x = cx + r * math.sin(L) * math.cos(lat)
        y = cy + r * math.sin(lat)
        ctx.save(); ctx.translate(x, y); ctx.scale(max(0.05, c) * rx * r, ry * r)
        ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        src(ctx, C['land']); ctx.fill()
    # terminator shading
    sg = cairo.RadialGradient(cx - r * 0.45, cy - r * 0.5, r * 0.2, cx - r * 0.2, cy - r * 0.2, r * 1.5)
    sg.add_color_stop_rgba(0, 1, 1, 1, 0.18); sg.add_color_stop_rgba(0.5, 0, 0, 0.1, 0)
    sg.add_color_stop_rgba(1, 0.02, 0.03, 0.15, 0.6)
    ctx.set_source(sg); ctx.paint()
    ctx.restore()

def chip_icon(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['white'])
    for i in (-14, 0, 14):
        for (x0, y0, x1, y1) in ((i, -26, i, -36), (i, 26, i, 36), (-26, i, -36, i), (26, i, 36, i)):
            ctx.move_to(x0, y0); ctx.line_to(x1, y1)
    ctx.stroke()
    rrect(ctx, -26, -26, 52, 52, 10); src(ctx, C['white']); ctx.fill()
    rrect(ctx, -12, -12, 24, 24, 5); src(ctx, col); ctx.fill()
    ctx.restore()

def card_icon(ctx, x, y, s, col):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -36, -24, 72, 48, 9); src(ctx, C['white']); ctx.fill()
    ctx.rectangle(-36, -12, 72, 10); src(ctx, col); ctx.fill()
    rrect(ctx, -26, 6, 18, 9, 3); src(ctx, col); ctx.fill()
    ctx.restore()

def code_icon(ctx, x, y, s, col):
    rich(ctx, [('</>', C['white'])], x, y - 4 * s, 48 * s, pop=False, shadow=False)

def bulb(ctx, x, y, s, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    glow(ctx, 0, 0, 260, C['yellow'], 0.7 + 0.15 * math.sin(t * 9))
    circle(ctx, 0, 0, 44, '#fff3b0')
    rrect(ctx, -20, 38, 40, 30, 7); src(ctx, '#9aa6cf'); ctx.fill()
    ctx.restore()

# ---------------------------------------------------------------- scenes
def scene1(ctx, lt, t):
    bg(ctx, t, glow_col='#3d2c96', gy=1150)
    ctx.save(); ctx.translate(540, 1250); ctx.scale(1.18, 1.18); ctx.translate(-540, -1180)
    # floating platform
    rrect(ctx, 150, 1350, 780, 64, 32); src(ctx, '#23338a'); ctx.fill()
    rrect(ctx, 150, 1350, 780, 18, 9); src(ctx, '#3550c0'); ctx.fill()
    shake = 0
    if 1.30 < lt < 1.65: shake = 10 * math.sin(lt * 90) * (1 - prog(lt, 1.3, 1.65))
    ctx.save(); ctx.translate(shake, 0)
    # desk
    rrect(ctx, 520, 1180, 360, 26, 13); src(ctx, '#4161d6'); ctx.fill()
    for lx in (550, 830):
        ctx.rectangle(lx, 1200, 18, 150); src(ctx, '#2c419b'); ctx.fill()
    grabbed = lt >= 1.38
    # robot path
    if lt < 1.38:
        p1 = eo(prog(lt, 0.45, 1.05)); p2 = ss(prog(lt, 1.05, 1.36))
        tx = lerp(860, 690, p1); ty = lerp(-260, 960, p1) + lerp(0, 120, p2)
        claw = lerp(0.2, 0.9, p1) * (1 - p2 * 0.0)
    else:
        p3 = ss(prog(lt, 1.55, 2.4))
        tx = lerp(690, 900, p3); ty = lerp(1080, -420, p3); claw = 0.25
    # person
    reach = 1.25 + 0.07 * math.sin(lt * 34)
    if grabbed:
        k = eback(prog(lt, 1.42, 1.62))
        armr = lerp(reach, 2.6, k); arml = lerp(0.2, 2.6, k)
    else:
        armr, arml = reach, 0.25 + 0.05 * math.sin(lt * 30 + 1)
    person(ctx, 420, 1352, 1.62, arm_l=arml, arm_r=armr)
    if not grabbed:
        laptop(ctx, 700, 1182, 1.0, t=t)
    base = (980, -90)
    carry = (lambda wx, wy: laptop(ctx, wx, wy + 200, 1.0, t=t)) if grabbed else None
    robot_arm(ctx, base, (tx, ty), claw=claw, carry=carry, t=t)
    ctx.restore(); ctx.restore()
    if grabbed:
        p = prog(lt, 1.45, 1.65)
        rich(ctx, [('?!', C['yellow'])], 404 + 8 * math.sin(lt * 40) * (1 - p), 880, 130, p)
    rich(ctx, [('AI just took', C['white'])], 540, 330, 96, prog(lt, -0.12, 0.2))
    rich(ctx, [('YOUR JOB.', C['pink'])], 540, 480, 165, prog(lt, 0.22, 0.5))

SPEED = [(random.uniform(60, 1020), random.uniform(0, H), random.uniform(80, 260), random.uniform(0.8, 1.4))
         for _ in range(34)]

def scene2(ctx, lt, t):
    bg(ctx, t, top='#0a0f33', bot='#2a1a66', glow_col='#5a2ea6', gy=1200, drift=lt * 900)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for (x, y, L, sp) in SPEED:
        yy = (y - lt * 2600 * sp) % (H + 300) - 150
        ctx.move_to(x, yy); ctx.line_to(x, yy + L); ctx.set_line_width(5)
        ctx.set_source_rgba(1, 1, 1, 0.18); ctx.stroke()
    bob = 30 * math.sin(lt * 4)
    glow(ctx, 540, 1150, 380, C['pink'], 0.25)
    person(ctx, 540, 1300 + bob, 1.55, shirt=C['orange'], arm_l=2.3 + 0.3 * math.sin(lt * 9),
           arm_r=2.1 + 0.3 * math.sin(lt * 9 + 2), rot=0.35 * math.sin(lt * 2.2) + lt * 0.5)
    rich(ctx, [('So... what happens', C['white'])], 540, 360, 86, prog(lt, 0.15, 0.4))
    rich(ctx, [('NOW?', C['yellow'])], 540, 560, 230, prog(lt, 0.65, 0.95))
    rich(ctx, [("Let's look at the ", C['white']), ('real numbers', C['cyan'])], 540, 1700, 56,
         prog(lt, 1.5, 1.75))

random.seed(3)
SLOTS = 52
order = list(range(SLOTS)); random.shuffle(order)
EMPTY0 = set(order[:12])                 # empty at start
REMOVED = set(order[12:24])              # 12 displaced
NEW = order[:12] + order[24:34]          # 22 new jobs
NEW_ORDER = {s: i for i, s in enumerate(NEW)}
PALETTE = [C['white'], '#ffd8b8', '#c9e8ff', '#ffe58a', '#b8f5d0']

def scene3(ctx, lt, t):
    bg(ctx, t, glow_col='#26408f', gy=1230)
    cx, cy, r = 540, 1230, 285
    rot = lt * 0.22
    planet(ctx, cx, cy, r, rot)
    for i in range(SLOTS):
        ang = 2 * math.pi * i / SLOTS + rot * 0.5 - math.pi / 2
        px, py = cx + (r + 2) * math.cos(ang), cy + (r + 2) * math.sin(ang)
        prot = ang + math.pi / 2
        col = PALETTE[i % len(PALETTE)]
        if i in REMOVED:
            redk = prog(lt, 0.6, 1.0); fly = eo(prog(lt, 1.0 + (i % 5) * 0.08, 2.0 + (i % 5) * 0.08))
            if fly >= 1: continue
            d = fly * 420
            col = C['red'] if redk > 0.5 else col
            mini(ctx, px + d * math.cos(ang), py + d * math.sin(ang), prot + fly * 3, 1.0, col, 1 - fly)
        elif i in NEW_ORDER:
            p = prog(lt, 2.35 + NEW_ORDER[i] * 0.045, 2.6 + NEW_ORDER[i] * 0.045)
            if p <= 0: continue
            glow(ctx, px + 20 * math.cos(ang), py + 20 * math.sin(ang), 45, C['green'], 0.6 * p)
            mini(ctx, px, py, prot, eback(p), C['green'])
        elif i not in EMPTY0:
            mini(ctx, px, py, prot, 1.0, col)
    # phase A
    fa = 1 - prog(lt, 2.0, 2.25)
    if fa > 0:
        ctx.save(); ctx.translate(0, -60 * (1 - fa))
        n = int(round(eo(prog(lt, 0.2, 1.3)) * 92))
        rich(ctx, [(f'−{n} MILLION', C['red'])], 540, 400, 140, prog(lt, 0.15, 0.4) * fa, pop=lt < 1)
        rich(ctx, [('jobs ', C['white']), ('displaced', C['red']), (' by 2030', C['white'])], 540, 540, 58,
             prog(lt, 0.4, 0.65) * fa, pop=lt < 1)
        ctx.restore()
    if lt > 2.05:
        n = int(round(eo(prog(lt, 2.15, 3.3)) * 170))
        rich(ctx, [(f'+{n} MILLION', C['green'])], 540, 400, 140, prog(lt, 2.1, 2.35))
        rich(ctx, [('NEW', C['green']), (' jobs created', C['white'])], 540, 540, 58, prog(lt, 2.3, 2.55))
    pb = prog(lt, 3.45, 3.7)
    if pb > 0:
        ctx.save(); ctx.translate(540, 1685); s = eback(pb); ctx.scale(s, s)
        rrect(ctx, -380, -58, 760, 116, 58); src(ctx, C['yellow'], clamp(pb * 2)); ctx.fill()
        ctx.restore()
        rich(ctx, [('Net result: +78 million jobs', C['dark'])], 540, 1683, 54, pb, shadow=False)
    source_line(ctx, 'Source: World Economic Forum, Future of Jobs Report 2025', prog(lt, 0.4, 0.8))

LIT = [0, 2, 3, 6, 7, 9]
LITCOL = [C['cyan'], C['pink'], C['yellow'], C['green'], C['orange'], '#b28cff']

def scene4(ctx, lt, t):
    bg(ctx, t, glow_col='#1f5a8f', gy=1100)
    rich(ctx, [('This has happened ', C['white']), ('before.', C['yellow'])], 540, 320, 74, prog(lt, 0.05, 0.3))
    n = int(round(eo(prog(lt, 0.4, 1.6)) * 60))
    rich(ctx, [(f'{n}%', C['cyan'])], 540, 590, 250, prog(lt, 0.35, 0.6))
    # years arrow
    pa = prog(lt, 0.5, 0.9)
    if pa > 0:
        rich(ctx, [('1940', C['grey'])], 230, 840, 50, pa, pop=False, shadow=False)
        rich(ctx, [('2018', C['white'])], 850, 840, 50, pa, pop=False, shadow=False)
        ctx.move_to(330, 840); ctx.line_to(lerp(330, 740, eo(prog(lt, 0.6, 1.2))), 840)
        ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['grey'], pa); ctx.stroke()
        if lt > 1.1:
            ctx.move_to(722, 822); ctx.line_to(746, 840); ctx.line_to(722, 858); ctx.stroke()
    for i in range(10):
        row, col = divmod(i, 5)
        x = 540 + (col - 2) * 172; y = 1110 + row * 230
        p = 0
        if i in LIT:
            k = LIT.index(i); p = prog(lt, 0.5 + k * 0.18, 0.7 + k * 0.18)
        bounce = -18 * math.sin(math.pi * p) if 0 < p < 1 else 0
        if p > 0:
            glow(ctx, x, y - 70, 130, LITCOL[LIT.index(i)], 0.5 * p)
            person(ctx, x, y + bounce, 0.58, shirt=LITCOL[LIT.index(i)], arm_l=0.2 + 2.2 * ss(p) * 0.5,
                   arm_r=0.2 + 2.2 * ss(p) * 0.5)
        else:
            person(ctx, x, y, 0.58, mono='#33458f')
    rich(ctx, [('of US jobs in 2018 were in roles', C['white'])], 540, 1480, 54, prog(lt, 1.3, 1.55))
    rich(ctx, [("that ", C['white']), ("didn't exist", C['cyan']), (' in 1940', C['white'])], 540, 1560, 54,
         prog(lt, 1.45, 1.7))
    source_line(ctx, 'Source: Autor et al., Quarterly Journal of Economics, 2024', prog(lt, 0.5, 0.9))

CARDS = [('AI & Machine Learning', 'specialists', C['pink'], chip_icon),
         ('FinTech', 'engineers', C['yellow'], card_icon),
         ('Software & App', 'developers', C['cyan'], code_icon)]

def scene5(ctx, lt, t):
    bg(ctx, t, glow_col='#4a2a9a', gy=1000)
    rich(ctx, [('Some of the ', C['white']), ('fastest-growing', C['green'])], 540, 330, 72, prog(lt, 0.05, 0.3))
    rich(ctx, [('jobs right now:', C['white'])], 540, 425, 72, prog(lt, 0.15, 0.4))
    for k, (t1, t2, col, icon) in enumerate(CARDS):
        p = eback(prog(lt, 0.45 + k * 0.25, 0.85 + k * 0.25), 1.4)
        if p <= 0: continue
        x = 90 + (1 - p) * 1100; y = 610 + k * 270
        rrect(ctx, x, y, 900, 220, 46); src(ctx, '#20307e'); ctx.fill()
        rrect(ctx, x, y, 900, 220, 46); ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke()
        glow(ctx, x + 125, y + 110, 120, col, 0.5)
        circle(ctx, x + 125, y + 110, 72, col)
        icon(ctx, x + 125, y + 110, 1.1, col)
        rich(ctx, [(t1, C['white'])], x + 230, y + 85, 54, pop=False, align='left', maxw=560)
        rich(ctx, [(t2, C['grey'])], x + 230, y + 148, 44, pop=False, align='left', w='normal', maxw=560)
        # bobbing up arrow
        ay = y + 110 - 8 * math.sin(t * 6 + k)
        ctx.move_to(x + 830, ay + 34); ctx.line_to(x + 830, ay - 30)
        ctx.move_to(x + 806, ay - 8); ctx.line_to(x + 830, ay - 34); ctx.line_to(x + 854, ay - 8)
        ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        src(ctx, C['green']); ctx.stroke()
    rich(ctx, [('...plus Big Data & security specialists', C['grey'])], 540, 1500, 44,
         prog(lt, 1.6, 1.85), w='normal')
    source_line(ctx, 'Source: World Economic Forum, Future of Jobs Report 2025', prog(lt, 0.5, 0.9))

def scene6(ctx, lt, t):
    bg(ctx, t, glow_col='#7a2f5e', gy=1000)
    rich(ctx, [('But here’s ', C['white']), ('the catch:', C['yellow'])], 540, 340, 88, prog(lt, 0.05, 0.3))
    lit = int(eo(prog(lt, 0.35, 1.35)) * 59 + 0.0001)
    for i in range(100):
        row, col = divmod(i, 10)
        x = 216 + col * 72; y = 560 + row * 72
        if i < lit:
            glow(ctx, x, y, 48, C['orange'], 0.45)
            circle(ctx, x, y, 25, C['orange'])
        else:
            circle(ctx, x, y, 25, '#2a3a86')
    rich(ctx, [('59', C['orange']), (' of every 100 workers', C['white'])], 540, 1390, 64, prog(lt, 1.15, 1.4))
    rich(ctx, [('will need ', C['white']), ('new skills', C['yellow']), (' by 2030', C['white'])], 540, 1480, 64,
         prog(lt, 1.35, 1.6))
    source_line(ctx, 'Source: World Economic Forum, Future of Jobs Report 2025', prog(lt, 0.4, 0.8))

def scene7(ctx, lt, t):
    bg(ctx, t, glow_col='#2e5bb8', gy=1100)
    cx, cy = 540, 1060
    # rays
    pr = eo(prog(lt, 0.0, 0.6))
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(lt * 0.35)
    for i in range(14):
        a0 = i * 2 * math.pi / 14
        ctx.move_to(0, 0); ctx.arc(0, 0, 1400, a0, a0 + 0.12); ctx.close_path()
    ctx.set_source_rgba(1, 0.86, 0.35, 0.10 * pr); ctx.fill()
    ctx.restore()
    # podium steps
    for i, hh in enumerate((70, 150, 250, 150, 70)):
        rrect(ctx, 115 + i * 170, 1570 - hh, 172, hh + 80, 18); src(ctx, '#2a3f9e'); ctx.fill()
        rrect(ctx, 115 + i * 170, 1570 - hh, 172, 18, 9); src(ctx, '#4a66d8'); ctx.fill()
    rise = eo(prog(lt, 0.0, 0.5))
    py = 1320 + (1 - rise) * 140
    by = py - 470
    icons = []
    for k, (ic, col) in enumerate(((chip_icon, C['pink']), (card_icon, C['yellow']), (code_icon, C['cyan']))):
        ang = lt * 1.6 + k * 2.094
        icons.append((math.sin(ang), cx + 370 * math.cos(ang), by + 90 * math.sin(ang), ic, col))
    def draw_icons(front):
        if rise < 0.02: return
        for d, ix, iy, ic, col in icons:
            if (d > 0) == front:
                sc = rise * (0.85 + 0.2 * d)
                circle(ctx, ix, iy, 56 * sc, col); ic(ctx, ix, iy, 0.85 * sc, col)
    draw_icons(False)
    if rise > 0.02: bulb(ctx, 545, by, rise, t)
    person(ctx, 545, py, 1.5, shirt=C['orange'], arm_l=2.75, arm_r=2.75)
    draw_icons(True)
    rich(ctx, [('AI isn’t ending work.', C['white'])], 540, 320, 80, prog(lt, 0.05, 0.3))
    rich(ctx, [('It’s ', C['white']), ('MOVING', C['yellow']), (' it.', C['white'])], 540, 480, 140,
         prog(lt, 0.45, 0.75))
    rich(ctx, [('Learn the next skill first.', C['cyan'])], 540, 1700, 56, prog(lt, 0.95, 1.2))
    source_line(ctx, 'Sources: WEF Future of Jobs Report 2025 · Autor et al., QJE 2024', prog(lt, 0.9, 1.2))

SCENES = [scene1, scene2, scene3, scene4, scene5, scene6, scene7]

def draw_scene(ctx, i, t, alpha=1.0, scale=1.0):
    ctx.save()
    ctx.translate(W / 2, H / 2); ctx.scale(scale, scale); ctx.translate(-W / 2, -H / 2)
    ctx.push_group()
    SCENES[i](ctx, t - S[i], t)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(alpha)
    ctx.restore()

def frame(ctx, t):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    idx = max(i for i in range(7) if t >= S[i]) if t < S[7] else 6
    # outgoing / incoming blending around boundaries
    drawn = False
    for b in range(1, 7):
        if abs(t - S[b]) < TR:
            x = ss((t - (S[b] - TR)) / (2 * TR))
            draw_scene(ctx, b - 1, t, 1.0, 1 + 0.12 * x)
            draw_scene(ctx, b, t, x, 0.9 + 0.1 * x)
            drawn = True
    if not drawn:
        draw_scene(ctx, idx, t)
    vignette(ctx)

def main():
    out = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'video'
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    if mode == 'stills':
        for t in [float(v) for v in sys.argv[3].split(',')]:
            frame(ctx, t); surf.write_to_png(f'{out}/f_{t:05.2f}.png')
        return
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                          '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(N):
        frame(ctx, f / FPS); surf.flush()
        p.stdin.write(bytes(surf.get_data()))
        if f % 60 == 0: print('frame', f, flush=True)
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    main()
