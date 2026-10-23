import cairo, math, random, sys, subprocess
from render import (W, H, FPS, C, hexc, clamp, prog, eo, ss, eback, lerp, src, rrect, circle, glow, bg,
                    vignette, font, rich, source_line, person)

S = [0.0, 5.2, 9.8, 14.4, 19.6, 23.6, 27.6, 31.0]
DUR = S[-1]
N = int(FPS * DUR)
TR = 0.16

LOOKS = [
    dict(skin='#f2c6a0', hair='#3a2353', style='short', shirt='#ff8a3d', iris='#3d7bd9'),
    dict(skin='#c68a5e', hair='#1d1433', style='long', shirt='#3ee0ff', iris='#5a3a1e'),
    dict(skin='#8d5a3b', hair='#120c22', style='curly', shirt='#ffd23f', iris='#3b2414'),
    dict(skin='#ffd9b8', hair='#b8562e', style='bun', shirt='#5ee38a', iris='#3f8f5a'),
    dict(skin='#e0a87c', hair='#5b5f7a', style='short', shirt='#b28cff', iris='#4a4a4a'),
    dict(skin='#f5cfae', hair='#2c1c12', style='long', shirt='#ff4f81', iris='#2f6fb0'),
]

def shade(col, k):
    r, g, b, a = hexc(col); return (r * k, g * k, b * k, a)

def face(ctx, cx, cy, s, L, blink=0.0, smile=1.0):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    if L['style'] == 'long':
        rrect(ctx, -142, -160, 284, 360, 130); src(ctx, L['hair']); ctx.fill()
    rrect(ctx, -215, 165, 430, 330, 160); src(ctx, L['shirt']); ctx.fill()
    rrect(ctx, -215, 165, 430, 50, 25); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.fill()
    rrect(ctx, -40, 70, 80, 120, 24); src(ctx, shade(L['skin'], 0.85)); ctx.fill()
    for sx in (-1, 1): circle(ctx, sx * 112, 10, 25, shade(L['skin'], 0.92))
    ctx.save(); ctx.scale(1, 140 / 116); circle(ctx, 0, 0, 116, L['skin']); ctx.restore()
    # hair cap
    ctx.save(); ctx.translate(0, -88); ctx.scale(1, 0.55); circle(ctx, 0, 0, 128, L['hair']); ctx.restore()
    if L['style'] == 'curly':
        for k in range(9):
            a = math.pi * (1.05 + 0.9 * k / 8)
            circle(ctx, 118 * math.cos(a), -70 + 95 * math.sin(a), 34, L['hair'])
    if L['style'] == 'bun':
        circle(ctx, 0, -165, 50, L['hair'])
    open_ = max(0.08, 1 - blink)
    for sx in (-1, 1):
        ex = sx * 45
        ctx.save(); ctx.translate(ex, -4); ctx.scale(1, open_)
        ctx.save(); ctx.scale(1, 16 / 25); circle(ctx, 0, 0, 25, '#ffffff'); ctx.restore()
        circle(ctx, 0, 0, 13, L['iris']); circle(ctx, 0, 0, 6.5, '#0d0a1e'); circle(ctx, 4, -4, 3.5, '#ffffff')
        ctx.restore()
        ctx.save(); ctx.translate(ex, -42); ctx.rotate(-sx * 0.08)
        rrect(ctx, -24, -5, 48, 11, 5); src(ctx, L['hair']); ctx.fill(); ctx.restore()
    ctx.move_to(2, 2); ctx.line_to(-8, 44); ctx.line_to(8, 48)
    ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    src(ctx, shade(L['skin'], 0.72)); ctx.stroke()
    ctx.arc(0, 62 - 10 * smile, 32, 0.18 * math.pi, 0.82 * math.pi)
    ctx.set_line_width(7); src(ctx, '#5a2a3a'); ctx.stroke()
    for sx in (-1, 1): circle(ctx, sx * 72, 42, 18, C['pink'], 0.22)
    ctx.restore()

def wire(ctx, cx, cy, s, a, t):
    """AI mesh over a face drawn with face(cx,cy,s)."""
    if a <= 0: return
    ctx.new_path()
    rx, ry = 120 * s, 145 * s
    ctx.save(); ctx.translate(cx, cy); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.save(); ctx.clip()
    rnd = random.Random(5)
    pts = {}
    for i in range(-6, 7):
        for j in range(-7, 8):
            pts[(i, j)] = (cx + i * rx / 5.2 + rnd.uniform(-6, 6) * s, cy + j * ry / 6.2 + rnd.uniform(-6, 6) * s)
    ctx.set_line_width(max(1.2, 2.4 * s))
    for (i, j), (x, y) in pts.items():
        for di, dj in ((1, 0), (0, 1), (1, 1)):
            q = pts.get((i + di, j + dj))
            if q: ctx.move_to(x, y); ctx.line_to(*q)
    src(ctx, C['cyan'], 0.75 * a); ctx.stroke()
    for (x, y) in pts.values(): circle(ctx, x, y, 3.2 * s, C['white'], 0.9 * a)
    sy = cy - ry + ((t * 1.2) % 1) * 2 * ry
    glow(ctx, cx, sy, rx * 1.1, C['cyan'], 0.35 * a)
    ctx.restore()
    ctx.save(); ctx.translate(cx, cy); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.set_line_width(4 * s); src(ctx, C['cyan'], a); ctx.stroke()

def glitched(ctx, draw, x, y, w, h, amt, seed):
    if amt <= 0.01:
        draw(ctx); return
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
    tc = cairo.Context(tmp); tc.translate(-x, -y); draw(tc)
    rnd = random.Random(seed)
    d = 26 * amt
    for col, dx in ((C['cyan'], -d), (C['pink'], d)):
        src(ctx, col, 0.6 * amt); ctx.mask_surface(tmp, x + dx, y)
    yy = 0
    while yy < h:
        bh = rnd.uniform(12, 70)
        off = rnd.uniform(-70, 70) * amt if rnd.random() < 0.55 else 0
        ctx.save(); ctx.rectangle(x - 200, y + yy, w + 400, bh); ctx.clip()
        ctx.set_source_surface(tmp, x + off, y); ctx.paint(); ctx.restore()
        yy += bh

def pill(ctx, x, y, txt, fill, tcol, size=40, p=1.0):
    if p <= 0: return
    font(ctx, size); w = ctx.text_extents(txt).x_advance + size * 1.1; h = size * 1.6
    ctx.save(); ctx.translate(x, y); s = eback(p); ctx.scale(s, s)
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2); src(ctx, fill); ctx.fill()
    ctx.restore()
    rich(ctx, [(txt, tcol)], x, y, size, p, shadow=False)

def ring_timer(ctx, x, y, r, frac, num, a):
    if a <= 0: return
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(16); ctx.set_source_rgba(1, 1, 1, 0.12 * a); ctx.stroke()
    ctx.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
    ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['yellow'], a); ctx.stroke()
    rich(ctx, [(str(num), C['yellow'])], x, y, 92, a, pop=False)

# ------------------------------------------------------------------ scenes
def scene1(ctx, lt, t):
    bg(ctx, t, glow_col='#4a2a9a', gy=1000)
    swap = prog(lt, 3.0, 3.2)
    if swap < 1:
        ctx.save(); ctx.translate(0, -50 * swap)
        rich(ctx, [('One of these faces', C['white'])], 540, 320, 84, prog(lt, -0.12, 0.2) * (1 - swap), pop=lt < 1)
        rich(ctx, [('is FAKE.', C['pink'])], 540, 465, 150, prog(lt, 0.15, 0.45) * (1 - swap), pop=lt < 1)
        ctx.restore()
    rich(ctx, [('Trick question:', C['white'])], 540, 320, 84, prog(lt, 3.25, 3.45))
    rich(ctx, [('BOTH', C['pink']), (' are fake.', C['white'])], 540, 465, 140, prog(lt, 3.45, 3.7))
    gl = math.sin(math.pi * prog(lt, 3.0, 3.5)) * (1.0 if lt < 3.5 else 0)
    for k, (x0, L) in enumerate(((60, LOOKS[3]), (580, LOOKS[2]))):
        pc = eback(prog(lt, -0.25 + 0.1 * k, 0.2 + 0.1 * k), 1.3)
        if pc <= 0: continue
        cx, cy = x0 + 220, 980
        blink = 1.0 if (lt + 1.3 + k * 0.7) % 2.6 < 0.12 else 0.0
        def draw(c, x0=x0, L=L, cx=cx, cy=cy, blink=blink, k=k):
            rrect(c, x0, 640, 440, 600, 44); src(c, '#23347f'); c.fill()
            c.save(); rrect(c, x0, 640, 440, 600, 44); c.clip()
            glow(c, cx, cy - 40, 360, L['shirt'], 0.35)
            face(c, cx, cy + 10, 0.86, L, blink)
            c.restore()
            rrect(c, x0, 640, 440, 600, 44); c.set_line_width(4); c.set_source_rgba(1, 1, 1, 0.14); c.stroke()
            circle(c, cx, 1240, 46, C['white'])
            rich(c, [('AB'[k], C['dark'])], cx, 1238, 52, pop=False, shadow=False)
        ctx.save(); ctx.translate(cx, 940); ctx.scale(pc, pc); ctx.translate(-cx, -940)
        glitched(ctx, draw, x0 - 10, 600, 460, 700, gl, int(t * 30) + k * 99)
        ctx.restore()
        wire(ctx, cx, cy + 10, 0.86, prog(lt, 3.3, 3.8), t)
        pill(ctx, cx, 690, 'AI-MADE', C['pink'], C['white'], 36, prog(lt, 3.55 + k * 0.1, 3.8 + k * 0.1))
    # countdown
    if lt < 3.05:
        a = prog(lt, 0.7, 0.9) * (1 - prog(lt, 2.9, 3.05))
        num = 3 - min(2, int(max(0, lt - 0.8) / 0.7))
        frac = 1 - clamp((lt - 0.8) / 2.1)
        ring_timer(ctx, 540, 1460, 82, frac, num, a)
    rich(ctx, [('You can no longer', C['white'])], 540, 1440, 66, prog(lt, 4.0, 4.25))
    rich(ctx, [('trust your eyes.', C['cyan'])], 540, 1550, 100, prog(lt, 4.15, 4.45))

WINNERS = {(17, 9), (34, 28)}

def scene2(ctx, lt, t):
    bg(ctx, t, glow_col='#26408f', gy=1050)
    rich(ctx, [('2,000 people', C['cyan']), (' took a', C['white'])], 540, 320, 76, prog(lt, 0.05, 0.3))
    rich(ctx, [('deepfake test.', C['white'])], 540, 420, 76, prog(lt, 0.15, 0.4))
    x0, y0, sp = 150, 560, 20
    for r in range(50):
        ap = prog(lt, 0.25 + r * 0.012, 0.4 + r * 0.012)
        if ap <= 0: continue
        for c in range(40):
            x, y = x0 + c * sp, y0 + r * sp
            win = (r, c) in WINNERS
            red = prog(lt, 1.2 + (r + c) * 0.009, 1.32 + (r + c) * 0.009)
            if win and lt > 2.0:
                continue
            col = lerp_col('#3a4fa8', C['red'], red if not win else 0)
            circle(ctx, x, y, 7, col, ap * (1 - 0.3 * red))
    if lt > 2.0:
        p = eback(prog(lt, 2.0, 2.3))
        for (r, c) in WINNERS:
            x, y = x0 + c * sp, y0 + r * sp
            for k in range(2):
                ph = ((lt - 2.0) * 0.9 + k * 0.5) % 1
                ctx.arc(x, y, 10 + ph * 90, 0, 2 * math.pi); ctx.set_line_width(4)
                src(ctx, C['green'], (1 - ph) * 0.8); ctx.stroke()
            glow(ctx, x, y, 80, C['green'], 0.8)
            circle(ctx, x, y, 13 * p, C['green'])
    rich(ctx, [('Only ', C['white']), ('2', C['green']), (' spotted every fake.', C['white'])], 540, 1640, 64,
         prog(lt, 2.3, 2.55))
    rich(ctx, [("That's 0.1%.", C['grey'])], 540, 1735, 50, prog(lt, 2.7, 2.95), w='normal')
    source_line(ctx, 'Source: iProov deepfake detection study, 2025 (UK & US)', prog(lt, 0.4, 0.8))

def lerp_col(a, b, k):
    A, B = hexc(a), hexc(b)
    return tuple(A[i] + (B[i] - A[i]) * k for i in range(4))

def bubble(ctx, x, y, txt, col, p):
    if p <= 0: return
    font(ctx, 44); w = ctx.text_extents(txt).x_advance + 60
    ctx.save(); ctx.translate(x, y); s = eback(p); ctx.scale(s, s)
    rrect(ctx, -w / 2, -42, w, 84, 30); src(ctx, col); ctx.fill()
    ctx.move_to(-14, 40); ctx.line_to(0, 66); ctx.line_to(14, 40); ctx.close_path(); ctx.fill()
    ctx.restore()
    rich(ctx, [(txt, C['dark'])], x, y, 44, p, shadow=False)

def scene3(ctx, lt, t):
    bg(ctx, t, glow_col='#5a2a8a', gy=950)
    rich(ctx, [('AI faces fooled people', C['white'])], 540, 320, 78, prog(lt, 0.05, 0.3))
    rich(ctx, [('2 out of 3', C['yellow']), (' times', C['white'])], 540, 445, 120, prog(lt, 0.25, 0.5))
    pc = eback(prog(lt, 0.1, 0.45), 1.3)
    L = LOOKS[5]
    if pc > 0:
        ctx.save(); ctx.translate(540, 930); ctx.scale(pc, pc); ctx.translate(-540, -930)
        rrect(ctx, 230, 570, 620, 720, 50); src(ctx, '#23347f'); ctx.fill()
        ctx.save(); rrect(ctx, 230, 570, 620, 720, 50); ctx.clip()
        glow(ctx, 540, 880, 480, L['shirt'], 0.3)
        blink = 1.0 if 2.9 < lt < 3.02 else 0.0
        face(ctx, 540, 900, 1.25, L, blink)
        sp = prog(lt, 0.35, 1.25)
        if 0 < sp < 1:
            sy = 570 + sp * 720
            glow(ctx, 540, sy, 380, C['cyan'], 0.35)
            ctx.rectangle(230, sy - 3, 620, 6); src(ctx, C['cyan']); ctx.fill()
        ctx.restore()
        ctx.restore()
        wire(ctx, 540, 900, 1.25, prog(lt, 2.3, 2.7) * 0.8, t)
        pill(ctx, 540, 610, 'AI-GENERATED', C['pink'], C['white'], 40, prog(lt, 2.3, 2.55))
    for k, (x, txt, col) in enumerate(((260, 'Real!', C['green']), (540, 'Real!', C['green']),
                                        (820, 'Fake', C['red']))):
        p = prog(lt, 0.2 + k * 0.1, 0.5 + k * 0.1)
        if p <= 0: continue
        person(ctx, x, 1740, 0.9, shirt=LOOKS[k]['shirt'], skin=LOOKS[k]['skin'], a=p)
        bubble(ctx, x, 1440, txt, col, prog(lt, 1.3 + k * 0.2, 1.55 + k * 0.2))
    source_line(ctx, 'Source: Miller et al., Psychological Science, 2023', prog(lt, 0.4, 0.8))

TILES = ['CFO', 'Finance', 'Legal', 'Ops', 'Manager', 'You']
TILE_BG = ['#2b3f9e', '#3b2a8f', '#1f5a8f', '#5a2a7a', '#2a4a7a', '#1f6a5a']

def scene4(ctx, lt, t):
    bg(ctx, t, glow_col='#7a2f5e', gy=1050)
    swap = prog(lt, 1.8, 2.0)
    if swap < 1:
        ctx.save(); ctx.translate(0, -50 * swap)
        rich(ctx, [('A worker joined a video call', C['white'])], 540, 320, 70, prog(lt, 0.05, 0.3) * (1 - swap),
             pop=lt < 1)
        rich(ctx, [('with his ', C['white']), ('CFO', C['yellow']), (' & colleagues.', C['white'])], 540, 420, 70,
             prog(lt, 0.2, 0.45) * (1 - swap), pop=lt < 1)
        ctx.restore()
    rich(ctx, [('Everyone else was', C['white'])], 540, 320, 76, prog(lt, 1.9, 2.1))
    rich(ctx, [('a DEEPFAKE.', C['pink'])], 540, 440, 130, prog(lt, 2.05, 2.3))
    pw = eback(prog(lt, 0.05, 0.4), 1.2)
    if pw <= 0: return
    ctx.save(); ctx.translate(540, 1050); ctx.scale(pw, pw); ctx.translate(-540, -1050)
    rrect(ctx, 60, 540, 960, 1010, 46); src(ctx, '#121a48'); ctx.fill()
    for i, c in enumerate((C['red'], C['yellow'], C['green'])): circle(ctx, 110 + i * 34, 585, 10, c)
    rich(ctx, [('Urgent: confidential transfer', C['grey'])], 600, 585, 30, pop=False, w='normal', shadow=False)
    gl = math.sin(math.pi * prog(lt, 1.75, 2.25))
    for i, name in enumerate(TILES):
        col, row = i % 2, i // 2
        x, y = 90 + col * 460, 625 + row * 305
        tw, th = 440, 290
        L = LOOKS[i] if i < 5 else LOOKS[0]
        talk = 1.0 if i == 0 and lt < 1.8 else 0
        def draw(c, x=x, y=y, L=L, i=i, name=name, talk=talk):
            rrect(c, x, y, tw, th, 28); src(c, TILE_BG[i]); c.fill()
            c.save(); rrect(c, x, y, tw, th, 28); c.clip()
            sm = 1.0 + 0.6 * math.sin(t * 18) * talk
            face(c, x + tw / 2, y + 150, 0.62, L, 1.0 if (t + i) % 3 < 0.1 else 0, sm)
            c.restore()
            if talk:
                rrect(c, x, y, tw, th, 28); c.set_line_width(7); src(c, C['green']); c.stroke()
            font(c, 30); w = c.text_extents(name).x_advance + 30
            rrect(c, x + 16, y + th - 56, w, 42, 14); c.set_source_rgba(0, 0, 0.1, 0.55); c.fill()
            rich(c, [(name, C['white'])], x + 16 + w / 2, y + th - 35, 30, pop=False, shadow=False)
        if i < 5:
            glitched(ctx, draw, x - 4, y - 4, tw + 8, th + 8, gl * (0.7 + 0.3 * ((i * 37) % 3)), int(t * 30) + i)
            if lt > 2.1:
                ctx.save(); rrect(ctx, x, y, tw, th, 28); ctx.clip()
                wire(ctx, x + tw / 2, y + 150, 0.62, prog(lt, 2.1, 2.4) * 0.8, t + i * 0.3)
                ctx.restore()
                rrect(ctx, x, y, tw, th, 28); ctx.set_line_width(6); src(ctx, C['red'], prog(lt, 2.1, 2.3)); ctx.stroke()
                pill(ctx, x + tw - 90, y + 44, 'FAKE', C['red'], C['white'], 32, prog(lt, 2.15 + i * 0.06, 2.4 + i * 0.06))
        else:
            draw(ctx)
            pill(ctx, x + tw - 90, y + 44, 'REAL', C['green'], C['dark'], 32, prog(lt, 2.5, 2.75))
    ctx.restore()
    n = int(round(eo(prog(lt, 2.8, 3.9)) * 25))
    rich(ctx, [(f'${n} MILLION', C['red'])], 540, 1665, 118, prog(lt, 2.75, 3.0))
    rich(ctx, [('wired to scammers in 15 transfers', C['grey'])], 540, 1765, 44, prog(lt, 3.1, 3.35), w='normal')
    source_line(ctx, 'Source: CNN, May 2024 (Arup case, Hong Kong)', prog(lt, 0.5, 0.9), y=1850)

def robot(ctx, x, y, s, talk, t):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -120); ctx.line_to(0, -175); ctx.set_line_width(10); src(ctx, C['steel']); ctx.stroke()
    glow(ctx, 0, -185, 60, C['pink'], 0.7); circle(ctx, 0, -185, 16, C['pink'])
    rrect(ctx, -150, -125, 300, 240, 70); src(ctx, C['steel']); ctx.fill()
    rrect(ctx, -150, -125, 300, 60, 30); ctx.set_source_rgba(1, 1, 1, 0.15); ctx.fill()
    rrect(ctx, -115, -80, 230, 150, 45); src(ctx, '#0f1640'); ctx.fill()
    for sx in (-1, 1):
        glow(ctx, sx * 50, -25, 60, C['cyan'], 0.6); circle(ctx, sx * 50, -25, 20, C['cyan'])
    for k in range(7):
        hh = 8 + 26 * talk * abs(math.sin(t * 14 + k * 1.3))
        rrect(ctx, -63 + k * 18, 35 - hh / 2, 10, hh, 5); src(ctx, C['cyan']); ctx.fill()
    ctx.restore()

WAVE = [0.25 + 0.75 * abs(math.sin(i * 0.9) * math.cos(i * 0.37)) for i in range(48)]

def scene5(ctx, lt, t):
    bg(ctx, t, glow_col='#1f5a8f', gy=1100)
    rich(ctx, [('AI can clone your voice', C['white'])], 540, 320, 76, prog(lt, 0.05, 0.3))
    rich(ctx, [('from just ', C['white']), ('3 SECONDS', C['yellow'])], 540, 440, 104, prog(lt, 0.25, 0.5))
    # speaker
    person(ctx, 165, 1040, 1.15, shirt=C['orange'], a=prog(lt, 0.0, 0.25))
    x0, yc = 290, 860
    grow = prog(lt, 0.2, 1.0)
    for i, v in enumerate(WAVE):
        if i / len(WAVE) > grow: break
        hh = 30 + 170 * v * (0.75 + 0.25 * math.sin(t * 8 + i))
        x = x0 + i * 15
        hi = i < 14
        col = C['yellow'] if hi and lt > 1.0 else C['cyan']
        rrect(ctx, x, yc - hh / 2, 9, hh, 4.5); src(ctx, col); ctx.fill()
    pb = prog(lt, 1.0, 1.25)
    if pb > 0:
        ctx.move_to(x0 - 6, 700); ctx.line_to(x0 - 6, 680); ctx.line_to(x0 + 14 * 15, 680); ctx.line_to(x0 + 14 * 15, 700)
        ctx.set_line_width(6); src(ctx, C['yellow'], pb); ctx.stroke()
        pill(ctx, x0 + 7 * 15, 630, '3 sec', C['yellow'], C['dark'], 36, pb)
    # copy flying to robot
    fp = ss(prog(lt, 1.35, 1.95))
    if 0 < fp < 1:
        for i in range(14):
            v = WAVE[i]; hh = (30 + 170 * v) * (1 - 0.4 * fp)
            x = lerp(x0 + i * 15, 470 + i * 10, fp); y = lerp(yc, 1330, fp) - math.sin(math.pi * fp) * 120
            rrect(ctx, x, y - hh / 2, 8, hh, 4); src(ctx, C['yellow'], 1 - 0.3 * fp); ctx.fill()
    pr = eback(prog(lt, 1.2, 1.5))
    if pr > 0:
        talk = 1.0 if lt > 2.0 else 0.0
        robot(ctx, 540, 1380, 1.1 * pr, talk, t)
        bubble(ctx, 540, 1615, '"Hi Mom, it\'s me..."', C['white'], prog(lt, 2.1, 2.35))
    source_line(ctx, 'Example: Alibaba Qwen3-TTS voice cloning, Dec 2025', prog(lt, 0.4, 0.8))

def phone_icon(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -22, -36, 44, 72, 10); src(ctx, C['white']); ctx.fill()
    rrect(ctx, -16, -28, 32, 50, 4); src(ctx, C['green']); ctx.fill()
    circle(ctx, 0, 29, 3.5, C['green']); ctx.restore()

def lock_icon(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.arc(0, -10, 18, math.pi, 2 * math.pi); ctx.set_line_width(8); src(ctx, C['white']); ctx.stroke()
    ctx.move_to(-18, -10); ctx.line_to(-18, 0); ctx.move_to(18, -10); ctx.line_to(18, 0); ctx.stroke()
    rrect(ctx, -28, -2, 56, 40, 8); src(ctx, C['white']); ctx.fill()
    circle(ctx, 0, 16, 6, C['yellow']); ctx.restore()

def glass_icon(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.arc(-6, -6, 22, 0, 2 * math.pi); ctx.set_line_width(9); src(ctx, C['white']); ctx.stroke()
    ctx.move_to(10, 10); ctx.line_to(30, 30); ctx.set_line_width(12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    ctx.restore()

TIPS = [('Call them back', 'on a number you already know', C['green'], phone_icon),
        ('Agree on a safe word', 'with family and coworkers', C['yellow'], lock_icon),
        ('Check the source', 'not just how real it looks', C['cyan'], glass_icon)]

def scene6(ctx, lt, t):
    bg(ctx, t, glow_col='#4a2a9a', gy=1000)
    rich(ctx, [('So how do you know', C['white'])], 540, 320, 76, prog(lt, 0.05, 0.3))
    rich(ctx, [("what's ", C['white']), ('REAL?', C['cyan'])], 540, 440, 120, prog(lt, 0.2, 0.45))
    for k, (t1, t2, col, icon) in enumerate(TIPS):
        p = eback(prog(lt, 0.45 + k * 0.28, 0.85 + k * 0.28), 1.4)
        if p <= 0: continue
        x = 90 + (1 - p) * 1100; y = 620 + k * 270
        rrect(ctx, x, y, 900, 220, 46); src(ctx, '#20307e'); ctx.fill()
        rrect(ctx, x, y, 900, 220, 46); ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke()
        glow(ctx, x + 125, y + 110, 120, col, 0.5)
        circle(ctx, x + 125, y + 110, 72, col); icon(ctx, x + 125, y + 110, 1.15)
        rich(ctx, [(t1, C['white'])], x + 230, y + 85, 56, pop=False, align='left', maxw=620)
        rich(ctx, [(t2, C['grey'])], x + 230, y + 150, 42, pop=False, align='left', w='normal', maxw=620)

def big_eye(ctx, cx, cy, s, openness, gl, t, seed):
    def draw(c):
        c.new_path(); c.save(); c.translate(cx, cy); c.scale(s, s * max(0.04, openness))
        c.move_to(-420, 0); c.curve_to(-200, -270, 200, -270, 420, 0); c.curve_to(200, 270, -200, 270, -420, 0)
        c.close_path(); path = c.copy_path()
        c.set_source_rgb(0.96, 0.97, 1.0); c.fill_preserve(); c.save(); c.clip()
        lx = 40 * math.sin(t * 0.9)
        g = cairo.RadialGradient(lx, 0, 20, lx, 0, 175)
        g.add_color_stop_rgba(0, *hexc('#7af0ff')); g.add_color_stop_rgba(0.6, *hexc('#2a7de0'))
        g.add_color_stop_rgba(1, *hexc('#1a2a8a'))
        c.set_source(g); c.arc(lx, 0, 175, 0, 2 * math.pi); c.fill()
        for k in range(24):
            a = k * 2 * math.pi / 24
            c.move_to(lx + 80 * math.cos(a), 80 * math.sin(a)); c.line_to(lx + 165 * math.cos(a), 165 * math.sin(a))
        c.set_line_width(4); c.set_source_rgba(1, 1, 1, 0.18); c.stroke()
        circle(c, lx, 0, 75, '#070a1e'); circle(c, lx + 45, -50, 26, '#ffffff', 0.9); circle(c, lx - 40, 45, 11, '#ffffff', 0.6)
        lg = cairo.LinearGradient(0, -260, 0, 0)
        lg.add_color_stop_rgba(0, 0.05, 0.08, 0.3, 0.45); lg.add_color_stop_rgba(1, 0.05, 0.08, 0.3, 0)
        c.set_source(lg); c.paint()
        c.restore()
        c.new_path(); c.append_path(path); c.set_line_width(26); src(c, '#1a2560'); c.stroke()
        c.restore()
    glow(ctx, cx, cy, 650 * s, C['cyan'], 0.35)
    glitched(ctx, draw, cx - 480 * s, cy - 320 * s, 960 * s, 640 * s, gl, seed)

def scene7(ctx, lt, t):
    bg(ctx, t, glow_col='#2e5bb8', gy=1000)
    rich(ctx, [('Your eyes can be ', C['white']), ('fooled.', C['pink'])], 540, 330, 82, prog(lt, 0.05, 0.3))
    bl = lt - 2.15
    openness = 1.0 - (math.sin(math.pi * clamp(bl / 0.26)) if 0 < bl < 0.26 else 0)
    openness *= eo(prog(lt, 0.0, 0.35))
    gl = math.sin(math.pi * prog(lt, 0.35, 0.75)) * 0.9
    big_eye(ctx, 540, 960, 1.0 + 0.04 * lt, openness, gl, t, int(t * 30))
    rich(ctx, [("Don't trust. ", C['white']), ('VERIFY.', C['yellow'])], 540, 1450, 112, prog(lt, 0.75, 1.0))
    rich(ctx, [('Follow for more AI reality checks', C['grey'])], 540, 1600, 46, prog(lt, 1.3, 1.55), w='normal')
    source_line(ctx, 'Sources: iProov 2025 · Psychological Science 2023 · CNN 2024 · Alibaba Qwen 2025',
                prog(lt, 1.2, 1.5))

SCENES = [scene1, scene2, scene3, scene4, scene5, scene6, scene7]

def draw_scene(ctx, i, t, alpha=1.0, scale=1.0):
    ctx.save()
    ctx.translate(W / 2, H / 2); ctx.scale(scale, scale); ctx.translate(-W / 2, -H / 2)
    ctx.push_group(); SCENES[i](ctx, t - S[i], t)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(alpha)
    ctx.restore()

# ------------------------------------------------------------------ transitions
OUT_S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
IN_S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
TRANS = {1: ('mosaic', 0.30), 2: ('iris', 0.32), 3: ('zoom', 0.40), 4: ('crt', 0.32), 5: ('stripes', 0.38),
         6: ('lids', 0.34)}

def ein(x): x = clamp(x); return x ** 3

def render_to(surf, i, t):
    c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
    SCENES[i](c, t - S[i], t); surf.flush(); return surf

def paint_surf(ctx, surf, alpha=1.0, sx=1.0, sy=None, cx=W / 2, cy=H / 2):
    sy = sx if sy is None else sy
    ctx.save(); ctx.translate(cx, cy); ctx.scale(sx, sy); ctx.translate(-cx, -cy)
    ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(alpha); ctx.restore()

def pixelate(ctx, surf, block, alpha=1.0):
    if block <= 1.05:
        ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(alpha); return
    sw, sh = max(1, int(W / block)), max(1, int(H / block))
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    sc = cairo.Context(small); sc.scale(sw / W, sh / H)
    sc.set_source_surface(surf, 0, 0); sc.get_source().set_filter(cairo.FILTER_GOOD); sc.paint()
    ctx.save(); ctx.scale(W / sw, H / sh); ctx.set_source_surface(small, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_NEAREST); ctx.paint_with_alpha(alpha); ctx.restore()

def t_mosaic(ctx, o, i, x, t):
    blk = 1 + 85 * (ein(x / 0.5) if x < 0.5 else ein((1 - x) / 0.5))
    mix = ss((x - 0.4) / 0.2)
    pixelate(ctx, o, blk)
    if mix > 0: pixelate(ctx, i, blk, mix)
    # chromatic tear near the peak
    peak = math.sin(math.pi * x) ** 4
    if peak > 0.05:
        rnd = random.Random(int(t * 30))
        for _ in range(7):
            y = rnd.uniform(0, H); h = rnd.uniform(20, 120)
            ctx.rectangle(0, y, W, h); src(ctx, rnd.choice([C['cyan'], C['pink'], C['yellow']]), 0.35 * peak); ctx.fill()

def t_iris(ctx, o, i, x, t):
    px, py = 150 + 9 * 20, 560 + 17 * 20
    paint_surf(ctx, o, 1.0, 1 + 0.06 * x, cx=px, cy=py)
    r = (ss(x) ** 1.4) * 2100
    if r > 1:
        ctx.save(); ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.clip()
        paint_surf(ctx, i, 1.0, 1.12 - 0.12 * x, cx=px, cy=py); ctx.restore()
        glow(ctx, px, py, r + 90, C['green'], 0.0)
        ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.set_line_width(36); src(ctx, C['green'], 0.35); ctx.stroke()
        ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.set_line_width(12); src(ctx, '#d6ffe4', 0.95); ctx.stroke()

def t_zoom(ctx, o, i, x, t):
    px, py = 540 - 45 * 1.25, 900 - 4 * 1.25
    if x < 0.55:
        k = x / 0.55
        z = math.exp(math.log(170) * k ** 2.0)
        paint_surf(ctx, o, 1.0, z, cx=px, cy=py)
        d = ss((k - 0.55) / 0.45)
        if d > 0: ctx.set_source_rgba(0.05, 0.04, 0.12, d); ctx.paint()
    else:
        k = (x - 0.55) / 0.45
        ctx.set_source_rgba(0.05, 0.04, 0.12, 1); ctx.paint()
        r = eo(k) * 1250
        if r > 1:
            ctx.save(); ctx.new_path(); ctx.arc(540, 960, r, 0, 2 * math.pi); ctx.clip()
            paint_surf(ctx, i, 1.0, 1.35 - 0.35 * eo(k)); ctx.restore()
            ctx.new_path(); ctx.arc(540, 960, r, 0, 2 * math.pi); ctx.set_line_width(14); src(ctx, C['cyan'], 1 - k); ctx.stroke()
        glow(ctx, 540, 960, 500, C['cyan'], 0.5 * (1 - k))

def crt(ctx, surf, k):
    """k=0 full picture, k=1 collapsed to a dot."""
    if k < 0.62:
        sy = 1 - ein(k / 0.62) * 0.995; sx = 1.0 + 0.04 * (k / 0.62)
    else:
        sy = 0.005; sx = 1.04 * (1 - ss((k - 0.62) / 0.38) * 0.985)
    paint_surf(ctx, surf, 1.0, sx, sy)
    flash = clamp(k * 1.3)
    ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(sx, sy)
    ctx.rectangle(-W / 2, -H / 2, W, H); ctx.set_source_rgba(0.85, 0.97, 1, 0.85 * flash); ctx.fill(); ctx.restore()
    glow(ctx, W / 2, H / 2, max(60, 700 * sx), C['cyan'], 0.6 * flash)

def t_crt(ctx, o, i, x, t):
    ctx.set_source_rgb(0.01, 0.01, 0.04); ctx.paint()
    if x < 0.5: crt(ctx, o, x / 0.5)
    else: crt(ctx, i, 1 - (x - 0.5) / 0.5)
    # scanlines
    a = math.sin(math.pi * x) * 0.25
    for y in range(0, H, 8):
        ctx.rectangle(0, y, W, 3)
    ctx.set_source_rgba(0, 0, 0, a); ctx.fill()

def band(ctx, E):
    ctx.new_path(); ctx.move_to(-2500, 0); ctx.line_to(E, 0); ctx.line_to(E - 0.4 * H, H); ctx.line_to(-2500, H); ctx.close_path()

def t_stripes(ctx, o, i, x, t):
    ctx.set_source_surface(o, 0, 0); ctx.paint()
    edges = [lerp(-300, 2250, ss(clamp((x - j * 0.12) / 0.64))) for j in range(4)]
    for j, col in enumerate((C['pink'], C['yellow'], C['cyan'])):
        band(ctx, edges[j]); src(ctx, col); ctx.fill()
        ctx.new_path(); ctx.move_to(edges[j], 0); ctx.line_to(edges[j] - 0.4 * H, H)
        ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.5); ctx.stroke()
    ctx.save(); band(ctx, edges[3]); ctx.clip()
    ctx.set_source_surface(i, 0, 0); ctx.paint(); ctx.restore()

def almond(ctx, cx, cy, hw, h):
    ctx.move_to(cx - hw, cy)
    ctx.curve_to(cx - hw * 0.5, cy - h / 0.75, cx + hw * 0.5, cy - h / 0.75, cx + hw, cy)
    ctx.curve_to(cx + hw * 0.5, cy + h / 0.75, cx - hw * 0.5, cy + h / 0.75, cx - hw, cy)
    ctx.close_path()

def t_lids(ctx, o, i, x, t):
    if x < 0.5:
        ctx.set_source_surface(o, 0, 0); ctx.paint(); h = 1450 * (1 - ein(x / 0.5))
    else:
        ctx.set_source_surface(i, 0, 0); ctx.paint(); k = (x - 0.5) / 0.5
        h = 1450 * eback(k, 1.2) * (1 - 0.35 * math.sin(math.pi * clamp(k / 0.5)) * (k < 0.5))
    ctx.new_path(); ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(-10, -10, W + 20, H + 20); almond(ctx, 540, 960, 1050, max(h, 0.5))
    src(ctx, '#05081a'); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    if h < 1400:
        ctx.new_path(); almond(ctx, 540, 960, 1050, max(h, 0.5))
        ctx.set_line_width(14); src(ctx, '#2a3a8a'); ctx.stroke()

TFUN = dict(mosaic=t_mosaic, iris=t_iris, zoom=t_zoom, crt=t_crt, stripes=t_stripes, lids=t_lids)

def frame(ctx, t):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    for b, (kind, hl) in TRANS.items():
        if S[b] - hl <= t < S[b] + hl:
            x = (t - (S[b] - hl)) / (2 * hl)
            render_to(OUT_S, b - 1, t)
            render_to(IN_S, b, S[b] + (t - S[b] + hl) / 2)
            TFUN[kind](ctx, OUT_S, IN_S, x, t)
            vignette(ctx); return
    idx = max(i for i in range(7) if t >= S[i])
    ctx.push_group(); SCENES[idx](ctx, t - S[idx], t); ctx.pop_group_to_source(); ctx.paint()
    vignette(ctx)

def main():
    out = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'video'
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    import json, numpy as np
    warp = json.load(open('vo/warp.json'))
    D = np.array([p[0] for p in warp['pairs']]); R = np.array([p[1] for p in warp['pairs']])
    tau = lambda tr: float(np.interp(tr, R, D))
    nframes = int(round(warp['total'] * FPS))
    if mode == 'stills':
        for t in [float(v) for v in sys.argv[3].split(',')]:
            frame(ctx, tau(t)); surf.write_to_png(f'{out}/w_{t:05.2f}.png')
        return
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium',
                          '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(nframes):
        frame(ctx, tau(f / FPS)); surf.flush()
        p.stdin.write(bytes(surf.get_data()))
        if f % 90 == 0: print('frame', f, flush=True)
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    main()
