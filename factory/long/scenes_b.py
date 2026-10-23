from base import *

# ===================================================================== 4  POLITICS
random.seed(31)
HOUSES = []
for row, (by, sc) in enumerate(((560, 0.55), (690, 0.7), (850, 0.9))):
    x = random.uniform(-20, 60)
    while x < W + 60:
        HOUSES.append((x, by + random.uniform(-14, 14) + 30 * math.sin(x / 260 + row), sc,
                       random.choice(['#ff8a3d', '#ffd23f', '#5ee38a', '#3ee0ff', '#ff4f81', '#b28cff']), row))
        x += random.uniform(110, 190) * sc
random.seed(32)
NODES = [(random.uniform(980, 1800), random.uniform(220, 860)) for _ in range(46)]
NODES[0] = (1060, 540)
EDGES = []
for i, (x, y) in enumerate(NODES):
    d = sorted(range(len(NODES)), key=lambda j: math.hypot(NODES[j][0] - x, NODES[j][1] - y))
    for j in d[1:4]:
        if (j, i) not in EDGES: EDGES.append((i, j))
HOPS = {0: 0}
frontier = [0]
while frontier:
    nxt = []
    for i in frontier:
        for a, b in EDGES:
            for u, v in ((a, b), (b, a)):
                if u == i and v not in HOPS: HOPS[v] = HOPS[i] + 1; nxt.append(v)
    frontier = nxt


def s4(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = [a for a, b in L]
    if lt < l3 + 0.2:
        bg(ctx, t, top='#0b1640', bot='#2a3a8a', glow_col='#3d5ab8', gy=700, stars=0.6)
        zoom = lerp(2.2, 1.0, eo(prog(lt, 0.0, l0 + 1.6)))
        ctx.save(); ctx.translate(960, 640); ctx.scale(zoom, zoom); ctx.translate(-960, -640)
        hills(ctx, 600, '#2a4a9a', amp=40, phase=0.3)
        hills(ctx, 720, '#25408a', amp=50, phase=1.3)
        hills(ctx, 880, '#1f357a', amp=40, phase=2.2)
        for n, (x, y, sc, col, row) in enumerate(HOUSES):
            house(ctx, x, y, sc, col)
            if l1 < lt < l3:
                ring_t = l1 + 0.8 + (n * 0.618 % 1) * 2.6
                p = prog(lt, ring_t, ring_t + 0.3)
                if p > 0 and n % 2 == 0:
                    ph = (t * 1.6 + n * 0.3) % 1
                    ctx.new_path(); ctx.arc(x, y - 110 * sc, 20 + ph * 40, -2.5, -0.64); ctx.set_line_width(5)
                    src(ctx, C['yellow'], (1 - ph) * p); ctx.stroke()
                    circle(ctx, x, y - 112 * sc, 10 * sc / 0.7 * p, C['yellow'])
        ctx.restore()
        title(ctx, [('A whole country', C['white'])], 150, 80, prog(lt, 0.4, 0.8) * (1 - prog(lt, l1 - 0.2, l1 + 0.1)))
        # big phone
        pp = eo(prog(lt, l1 + 0.2, l1 + 0.8))
        if pp > 0:
            px = lerp(-300, 360, pp)
            ctx.set_source_rgba(0.03, 0.05, 0.16, 0.45 * pp); ctx.paint()
            phone(ctx, px, 500, 1.5, ring=1.0 if lt < l2 else 0.0, t=t)
            rich(ctx, [('Incoming call', C['white'])], px, 310, 30, 1, pop=False, w='normal', shadow=False)
            wave_bars(ctx, px - 110, 500, 14, 16, 110, t, C['cyan'], seed=4)
            text_left(ctx, [('New Hampshire · January 2024', C['grey'])], 760, 300, 40, prog(lt, l1 + 0.6, l1 + 0.9), w='normal')
            bubble(ctx, 1150, 470, '"...skip the primary."', C['white'], prog(lt, L[1][1] - 1.6, L[1][1] - 1.3))
            stamp(ctx, px, 500, 'FAKE', C['red'], prog(lt, l2 + 0.1, l2 + 0.35), size=110)
            pg = prog(lt, l2 + 1.0, l2 + 1.4)
            if pg > 0:
                gx, gy = 1180, 720
                ang = -0.9 + 0.9 * eo(prog(lt, l2 + 1.0, l2 + 1.35))
                ctx.save(); ctx.translate(gx, gy); ctx.rotate(ang)
                rrect(ctx, -12, -160, 24, 160, 12); src(ctx, '#8c6a45', pg); ctx.fill()
                rrect(ctx, -70, -210, 140, 70, 20); src(ctx, '#b0875a', pg); ctx.fill(); ctx.restore()
                rrect(ctx, gx - 110, gy + 10, 220, 40, 14); src(ctx, '#6b4f33', pg); ctx.fill()
                v = 6_000_000 * eo(prog(lt, l2 + 1.35, l2 + 2.3))
                rich(ctx, [('$' + counter_text(v), C['yellow'])], 1520, 690, 90, prog(lt, l2 + 1.3, l2 + 1.55))
                rich(ctx, [('fine', C['grey'])], 1520, 780, 44, prog(lt, l2 + 1.5, l2 + 1.75), w='normal')
        source_line(ctx, 'Sources: NPR / WBUR (FCC, 2024)', prog(lt, l1 + 1, l1 + 1.4))
        if lt < l3 - 0.2: return
    # ---- Slovakia network
    a3 = prog(lt, l3 - 0.2, l3 + 0.3)
    ctx.push_group()
    bg(ctx, t, glow_col='#6a2a6a', gy=540)
    text_left(ctx, [('Slovakia', C['white'])], 150, 300, 96, prog(lt, l3 + 0.2, l3 + 0.5), pop=True)
    text_left(ctx, [('2 days before', C['yellow'])], 150, 410, 64, prog(lt, l3 + 0.6, l3 + 0.9))
    text_left(ctx, [('the election', C['white'])], 150, 490, 64, prog(lt, l3 + 0.75, l3 + 1.05))
    spread = (lt - l3 - 1.2) / 0.35
    for a, b in EDGES:
        on = min(HOPS.get(a, 99), HOPS.get(b, 99)) < spread - 0.5
        (x0, y0), (x1, y1) = NODES[a], NODES[b]
        ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_line_width(4 if on else 2)
        src(ctx, C['red'] if on else '#3a4a9a', 0.8 if on else 0.6); ctx.stroke()
    for i, (x, y) in enumerate(NODES):
        hop = HOPS.get(i, 99)
        on = spread > hop
        k = prog(spread, hop, hop + 0.4)
        if on: glow(ctx, x, y, 60, C['red'], 0.5 * k)
        circle(ctx, x, y, 18 if i else 30, C['red'] if on else '#5a6ab8')
        if on and k < 1:
            ctx.new_path(); ctx.arc(x, y, 18 + 50 * k, 0, 2 * math.pi); ctx.set_line_width(4); src(ctx, C['red'], 1 - k); ctx.stroke()
    x0, y0 = NODES[0]
    wave_bars(ctx, x0 - 50, y0 - 80, 9, 12, 46, t, C['yellow'], seed=7)
    pill(ctx, x0, y0 + 70, 'FAKE AUDIO', C['red'], C['white'], 28, prog(lt, l3 + 1.0, l3 + 1.3))
    pq = prog(lt, l4 + 0.2, l4 + 0.6)
    if pq > 0:
        ctx.set_source_rgba(0.03, 0.05, 0.16, 0.5 * pq); ctx.paint()

        def box():
            rrect(ctx, 820, 470, 280, 260, 24); src(ctx, '#e8ecff'); ctx.fill()
            rrect(ctx, 880, 470, 160, 20, 8); src(ctx, '#1b2a6e'); ctx.fill()
            rrect(ctx, 905, 380, 110, 120, 10); src(ctx, C['white']); ctx.fill()
            ctx.move_to(930, 430); ctx.line_to(955, 455); ctx.line_to(995, 405); ctx.set_line_width(10); src(ctx, C['green'])
            ctx.stroke()
        pop_scale(ctx, 960, 600, pq, box)
        rich(ctx, [('?', C['yellow'])], 1130, 420 + 10 * math.sin(t * 4), 160, prog(lt, l4 + 0.6, l4 + 0.9))
        title(ctx, [('Did it change the result? ', C['white']), ('Still debated.', C['yellow'])], 830, 56,
              prog(lt, l4 + 1.0, l4 + 1.3))
    source_line(ctx, 'Source: Harvard Kennedy School Misinformation Review, 2024', prog(lt, l3 + 1, l3 + 1.4))
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a3)


# ===================================================================== 5  LIAR'S DIVIDEND
random.seed(41)
CRACKS = []
for k in range(9):
    ang = k * 2 * math.pi / 9 + random.uniform(-0.2, 0.2)
    pts = [(0, 0)]; r = 0
    while r < 520:
        r += random.uniform(50, 110); a_ = ang + random.uniform(-0.25, 0.25)
        pts.append((r * math.cos(a_), r * math.sin(a_)))
    CRACKS.append(pts)


def photo(ctx, x, y, w, h, lt, t, crack=0.0):
    rrect(ctx, x - 24, y - 24, w + 48, h + 110, 14); src(ctx, '#f4efe6'); ctx.fill()
    ctx.save(); rrect(ctx, x, y, w, h, 6); ctx.clip()
    g = cairo.LinearGradient(0, y, 0, y + h); g.add_color_stop_rgba(0, *hexc('#3b5bd6')); g.add_color_stop_rgba(1, *hexc('#1f2f7a'))
    ctx.set_source(g); ctx.paint()
    hills(ctx, y + h - 60, '#2a3f9e', amp=0)
    ctx.rectangle(x, y + h - 80, w, 80); src(ctx, '#2a3f9e'); ctx.fill()
    # a figure sneaking off with a money bag
    person(ctx, x + w * 0.45, y + h - 30, 1.15, shirt='#5a5f7a', arm_l=1.0, arm_r=2.0)
    circle(ctx, x + w * 0.45 + 95, y + h - 260, 46, '#b0875a')
    rich(ctx, [('$', C['dark'])], x + w * 0.45 + 95, y + h - 256, 44, pop=False, shadow=False)
    ctx.restore()
    if crack > 0:
        ctx.save(); ctx.translate(x + w * 0.6, y + h * 0.4)
        for pts in CRACKS:
            n = len(pts); m = crack * (n - 1)
            ctx.move_to(*pts[0])
            for i in range(1, n):
                if i > m + 1: break
                px, py = pts[i]
                if i > m:
                    f = m - (i - 1); qx, qy = pts[i - 1]; px, py = lerp(qx, px, f), lerp(qy, py, f)
                ctx.line_to(px, py)
        ctx.set_line_width(5); ctx.set_source_rgba(1, 1, 1, 0.9); ctx.stroke(); ctx.restore()


def s5(ctx, lt, t, L):
    l0, l1, l2, l3 = [a for a, b in L]
    dark = prog(lt, 0.2, l1)
    bg(ctx, t, top=lerp_col('#0b1640', '#05061a', dark), bot=lerp_col('#1c2d72', '#140c2e', dark),
       glow_col='#4a1f5a', gy=540, stars=1 - 0.6 * dark)
    pp = eback(prog(lt, 0.3, 0.9))
    shift = ss(prog(lt, l2 - 0.3, l2 + 0.5))
    if pp > 0:
        px = lerp(660, 420, shift)
        crack = eo(prog(lt, l1 + 0.3, l1 + 1.3))
        def ph():
            photo(ctx, px, 240, 680, 480, lt, t, crack)
            rich(ctx, [('CAUGHT ON CAMERA', C['dark'])], px + 340, 790, 40, pop=False, shadow=False)
        ctx.save(); ctx.translate(px + 380, 480); ctx.rotate(-0.03); ctx.translate(-px - 380, -480)
        pop_scale(ctx, px + 380, 480, pp, ph); ctx.restore()
        fl = prog(lt, 1.0, 1.4)
        if 0 < fl < 1: ctx.set_source_rgba(1, 1, 1, 0.7 * (1 - fl)); ctx.paint()
        pill(ctx, px + 610, 270, 'REAL', C['green'], C['dark'], 36, prog(lt, 1.2, 1.5))
        if lt > l2 + 1.2:
            stamp(ctx, px + 610, 270, '?', C['yellow'], prog(lt, l2 + 2.2, l2 + 2.45), size=80)
    if lt > l2:
        pin = eo(prog(lt, l2 + 0.2, l2 + 0.8))
        cx = lerp(2100, 1500, pin)
        shrug = ss(prog(lt, l2 + 1.6, l2 + 2.0))
        person(ctx, cx, 860, 1.9, shirt='#5a5f7a', arm_l=lerp(0.2, 2.3, shrug), arm_r=lerp(0.2, 2.3, shrug))
        bubble(ctx, cx - 40, 380, '"That\'s just AI!"', C['white'], prog(lt, l2 + 2.0, l2 + 2.3))
        if lt > l3:
            for k in range(18):
                p = prog(lt, l3 + 0.3 + k * 0.12, l3 + 1.1 + k * 0.12)
                if 0 < p:
                    x = cx + 120 * math.sin(k * 2.3); y = lerp(-60, 560, p ** 1.6)
                    coin(ctx, x, y, 26, 1 - prog(p, 0.85, 1.0))
            title(ctx, [("THE LIAR'S ", C['white']), ('DIVIDEND', C['yellow'])], 120, 100, prog(lt, l3 + 0.4, l3 + 0.75))
            source_line(ctx, 'Concept: Chesney & Citron, California Law Review, 2019', prog(lt, l3 + 0.6, l3 + 1.0))
    title(ctx, [("It's what they do ", C['white']), ('to the truth.', C['pink'])], 120, 64,
          prog(lt, l1 + 0.2, l1 + 0.5) * (1 - prog(lt, l2 - 0.2, l2 + 0.1)))


# ===================================================================== 6  FIGHTING BACK
def eu_stars(ctx, cx, cy, r, p, t):
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        q = eback(prog(p, k / 14, k / 14 + 0.2))
        if q <= 0: continue
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        ctx.save(); ctx.translate(x, y); ctx.scale(q, q); ctx.new_path()
        for i in range(10):
            rr = 22 if i % 2 == 0 else 9; aa = -math.pi / 2 + i * math.pi / 5
            ctx.line_to(rr * math.cos(aa), rr * math.sin(aa))
        ctx.close_path(); src(ctx, C['yellow']); ctx.fill(); ctx.restore()


def s6(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = [a for a, b in L]
    warm = ss(prog(lt, 0.4, 2.0))
    bg(ctx, t, top=lerp_col('#0b1640', '#1a2a6e', warm), bot=lerp_col('#1c2d72', '#5a3a8a', warm),
       glow_col=lerp_col('#35237e', '#ff8a3d', warm * 0.7), gy=980, gr=1100)
    # ---- line 0: shield
    a0 = 1 - ss(prog(lt, l1 - 0.3, l1 + 0.1))
    if a0 > 0:
        ctx.push_group()
        rise = eback(prog(lt, l0 + 0.9, l0 + 1.5))
        if rise > 0:
            cx, cy = 960, 560 + (1 - rise) * 200
            glow(ctx, cx, cy, 380, C['cyan'], 0.5)
            ctx.save(); ctx.translate(cx, cy); ctx.scale(rise, rise)
            ctx.move_to(0, -200); ctx.curve_to(110, -150, 160, -160, 170, -150); ctx.curve_to(170, 40, 110, 140, 0, 210)
            ctx.curve_to(-110, 140, -170, 40, -170, -150); ctx.curve_to(-160, -160, -110, -150, 0, -200); ctx.close_path()
            src(ctx, '#2f6fb0'); ctx.fill_preserve(); ctx.set_line_width(14); src(ctx, C['cyan']); ctx.stroke()
            ctx.move_to(-70, 0); ctx.line_to(-15, 60); ctx.line_to(80, -60); ctx.set_line_width(26)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['white']); ctx.stroke(); ctx.restore()
        title(ctx, [('Doomed? ', C['white']), ('Not quite.', C['cyan'])], 170, 80, prog(lt, l0 + 0.8, l0 + 1.1))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a0)
    # ---- lines 1-2: watermark + content credentials
    if l1 - 0.3 < lt < l3 + 0.2:
        a1 = prog(lt, l1 - 0.2, l1 + 0.2) * (1 - prog(lt, l3 - 0.3, l3 + 0.1))
        ctx.push_group()
        slide = ss(prog(lt, l2 - 0.2, l2 + 0.6))
        px, py, pw, phh = lerp(560, 260, slide), 230, 800, 560
        card(ctx, px - 16, py - 16, pw + 32, phh + 32, '#f4efe6', 20, stroke=False)
        ctx.save(); rrect(ctx, px, py, pw, phh, 8); ctx.clip()
        g = cairo.LinearGradient(0, py, 0, py + phh); g.add_color_stop_rgba(0, *hexc('#ff9a6a')); g.add_color_stop_rgba(1, *hexc('#ffd28a'))
        ctx.set_source(g); ctx.paint()
        circle(ctx, px + 560, py + 260, 90, '#fff3c8')
        ctx.save(); ctx.translate(px - 960 * 0 , py + phh - 1080 + 0)
        ctx.restore()
        ctx.new_path(); ctx.move_to(px, py + phh)
        for xx in range(0, pw + 41, 40):
            ctx.line_to(px + xx, py + 380 - 60 * math.sin(xx / 160) - 30 * math.sin(xx / 70))
        ctx.line_to(px + pw, py + phh); ctx.close_path(); src(ctx, '#6a4aa8'); ctx.fill()
        ctx.new_path(); ctx.move_to(px, py + phh)
        for xx in range(0, pw + 41, 40):
            ctx.line_to(px + xx, py + 460 - 40 * math.sin(xx / 120 + 1))
        ctx.line_to(px + pw, py + phh); ctx.close_path(); src(ctx, '#3a2a7a'); ctx.fill()
        # scanner reveals watermark
        sc = prog(lt, l1 + 0.8, l1 + 2.6)
        if 0 < sc and lt < l2 + 0.3:
            sy = py + sc * phh
            ctx.save(); ctx.rectangle(px, py, pw, sy - py); ctx.clip()
            for yy in range(int(py) + 10, int(py + phh), 26):
                for xx in range(int(px) + 10, int(px + pw), 26):
                    v = math.sin(xx * 0.05) * math.cos(yy * 0.05)
                    circle(ctx, xx, yy, 3 + 3 * abs(v), C['cyan'], 0.55)
            ctx.restore()
            glow(ctx, px + pw / 2, sy, 420, C['cyan'], 0.4)
            ctx.rectangle(px, sy - 3, pw, 6); src(ctx, C['cyan']); ctx.fill()
        ctx.restore()
        pill(ctx, px + pw / 2, py - 10, 'invisible watermark', C['cyan'], C['dark'], 34, prog(lt, l1 + 1.6, l1 + 1.9) * (1 - slide))
        # credentials panel
        pc = eback(prog(lt, l2 + 0.6, l2 + 1.0), 1.2)
        if pc > 0:
            def panel():
                card(ctx, 1150, 210, 600, 620, '#f4f6ff', 30, stroke=False)
                circle(ctx, 1220, 280, 34, C['cyan'])
                rich(ctx, [('i', C['dark'])], 1220, 282, 40, pop=False, shadow=False)
                rich(ctx, [('Content Credentials', C['dark'])], 1275, 280, 40, pop=False, align='left', shadow=False)
                rows = [('Captured with', 'Camera'), ('Date', 'Mar 12, 2026'), ('Edited', 'Crop, color'),
                        ('AI used', 'None'), ('Signed', 'Verified')]
                for i, (k, v) in enumerate(rows):
                    p = prog(lt, l2 + 1.2 + i * 0.35, l2 + 1.5 + i * 0.35)
                    if p <= 0: continue
                    y = 380 + i * 88
                    rrect(ctx, 1185, y - 32, 530, 64, 16); src(ctx, '#e3e8fa', p); ctx.fill()
                    rich(ctx, [(k, '#6b7fb8')], 1210, y, 30, p, pop=False, align='left', shadow=False, w='normal')
                    rich(ctx, [(v, C['dark'] if i < 4 else '#2f8f58')], 1690 - 10, y, 32, p, pop=False, shadow=False,
                         align='left', maxw=260) if False else None
                    font(ctx, 32); ww = ctx.text_extents(v).x_advance
                    rich(ctx, [(v, C['dark'] if i < 4 else '#2f8f58')], 1690 - ww, y, 32, p, pop=False, shadow=False, align='left')
            pop_scale(ctx, 1450, 520, pc, panel)
            ctx.move_to(px + pw + 16, 500); ctx.line_to(1150, 500); ctx.set_line_width(6); ctx.set_dash([14, 12])
            src(ctx, C['cyan'], pc); ctx.stroke(); ctx.set_dash([])
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a1)
    # ---- line 3: laws
    if l3 - 0.3 < lt < l4 + 0.2:
        a3 = prog(lt, l3 - 0.2, l3 + 0.2) * (1 - prog(lt, l4 - 0.3, l4 + 0.1))
        ctx.push_group()
        title(ctx, [('Laws are catching up', C['white'])], 150, 72, prog(lt, l3 + 0.1, l3 + 0.4))
        pe = prog(lt, l3 + 1.0, l3 + 2.2)
        eu_stars(ctx, 560, 480, 200, pe, t)
        pv = eback(prog(lt, l3 + 1.6, l3 + 2.0))
        if pv > 0:
            def vid():
                rrect(ctx, 420, 390, 280, 180, 20); src(ctx, '#0f1640'); ctx.fill()
                face(ctx, 560, 440, 0.3, LOOKS[4])
                
            pop_scale(ctx, 560, 480, pv, vid)
            pill(ctx, 560, 600, 'AI-GENERATED', C['pink'], C['white'], 30, prog(lt, l3 + 2.4, l3 + 2.7))
        rich(ctx, [('EU · since Aug 2026', C['grey'])], 560, 745, 38, prog(lt, l3 + 1.2, l3 + 1.5), w='normal')
        rich(ctx, [('deepfakes must be labeled', C['white'])], 560, 800, 42, prog(lt, l3 + 2.2, l3 + 2.5))
        # US 48h
        pu = prog(lt, l3 + 3.8, l3 + 4.2)
        if pu > 0:
            frac = 1 - prog(lt, l3 + 4.4, L[3][1])
            ring_timer(ctx, 1360, 480, 170, frac, '48h', pu)
            rich(ctx, [('USA · TAKE IT DOWN Act', C['grey'])], 1360, 745, 38, pu, w='normal')
            rich(ctx, [('removal within 48 hours', C['white'])], 1360, 800, 42, prog(lt, l3 + 4.6, l3 + 4.9))
        source_line(ctx, 'Sources: EU AI Act, Art. 50 · TAKE IT DOWN Act (US, 2025)', prog(lt, l3 + 1, l3 + 1.4))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a3)
    # ---- line 4: arms race loop
    if lt > l4 - 0.3:
        a4 = prog(lt, l4 - 0.2, l4 + 0.2)
        ctx.push_group()
        cx, cy, r = 960, 500, 280
        spin = (lt - l4) * (0.9 + 0.5 * (lt - l4))
        ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_line_width(16); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke()
        for k in range(2):
            a0_ = spin + k * math.pi
            ctx.new_path(); ctx.arc(cx, cy, r, a0_, a0_ + 2.4); ctx.set_line_width(16); src(ctx, [C['pink'], C['cyan']][k]); ctx.stroke()
            ex, ey = cx + r * math.cos(a0_ + 2.4), cy + r * math.sin(a0_ + 2.4)
            ang = a0_ + 2.4 + math.pi / 2
            ctx.move_to(ex + 34 * math.cos(ang), ey + 34 * math.sin(ang))
            ctx.line_to(ex + 30 * math.cos(ang - 2.2), ey + 30 * math.sin(ang - 2.2))
            ctx.line_to(ex + 30 * math.cos(ang + 2.2), ey + 30 * math.sin(ang + 2.2)); ctx.close_path()
            src(ctx, [C['pink'], C['cyan']][k]); ctx.fill()
        robot2(ctx, cx - 560, 820, 0.8, '#c24a8a', C['pink'], 'forger', t, look=0.6, arm=0.3 * math.sin(t * 9))
        robot2(ctx, cx + 560, 820, 0.8, '#2f6fb0', C['cyan'], 'detective', t, look=-0.6)
        v = 1 + int(max(0, lt - l4 - 0.5) * (2 + (lt - l4)))
        rich(ctx, [(f'v{v}', C['white'])], cx, cy - 40, 120, prog(lt, l4 + 0.3, l4 + 0.6), pop=False)
        rich(ctx, [('arms race', C['grey'])], cx, cy + 70, 50, prog(lt, l4 + 0.5, l4 + 0.8), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a4)


# ===================================================================== 7  OUTRO
FLAGS = [('URGENT', C['red']), ('EMOTIONAL', C['pink']), ('MONEY', C['yellow']), ('SECRECY', C['orange'])]
TIPS = [('Call back', 'on a number you know', C['green'], phone_icon),
        ('Safe word', 'agree on one with family', C['yellow'], lock_icon),
        ('Check the source', 'not just how real it looks', C['cyan'], glass_icon)]


def s7(ctx, lt, t, L):
    l0, l1, l2, l3, l4, l5 = [a for a, b in L]
    sun = ss(prog(lt, l3 - 0.3, l3 + 0.6)) * (1 - ss(prog(lt, l4 - 0.2, l4 + 0.6)))
    bg(ctx, t, top=lerp_col('#0b1640', '#2a2a7a', sun), bot=lerp_col('#1c2d72', '#ff8a5a', sun),
       glow_col=lerp_col('#35237e', '#ffd23f', sun), gy=lerp(560, 820, sun))
    # ---- line 0: skepticism
    if lt < l1 + 0.2:
        a = 1 - prog(lt, l1 - 0.2, l1 + 0.2)
        ctx.push_group()
        ph = eback(prog(lt, 0.3, 0.8))
        if ph > 0:
            ctx.save(); ctx.translate(960, 560); ctx.scale(ph, ph)
            ctx.new_path(); ctx.arc(0, -40, 220, math.pi * 0.85, math.pi * 2.15)
            ctx.curve_to(220, 120, 170, 170, 150, 260); ctx.line_to(-80, 260); ctx.curve_to(-90, 200, -130, 190, -190, 180)
            ctx.curve_to(-200, 130, -230, 90, -205, 40); ctx.close_path(); src(ctx, '#2a3f9e'); ctx.fill()
            glow(ctx, 0, -40, 220, C['yellow'], 0.6 + 0.1 * math.sin(t * 5))
            ctx.restore()
            rich(ctx, [('?', C['yellow'])], 960, 520, 260 * ph, 1, pop=False)
        title(ctx, [('healthy ', C['white']), ('skepticism', C['yellow'])], 150, 80, prog(lt, L[0][1] - 1.2, L[0][1] - 0.9))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 1: red flags
    if l1 - 0.2 < lt < l2 + 0.2:
        a = prog(lt, l1 - 0.2, l1 + 0.2) * (1 - prog(lt, l2 - 0.2, l2 + 0.2))
        ctx.push_group()
        phone(ctx, 640, 480, 1.7, t=t)
        pm = eback(prog(lt, l1 + 0.2, l1 + 0.5))
        if pm > 0:
            def msg():
                rrect(ctx, 500, 300, 280, 130, 24); src(ctx, C['white']); ctx.fill()
                for i, wl in enumerate((220, 180, 120)):
                    rrect(ctx, 525, 325 + i * 32, wl, 16, 8); src(ctx, '#c9d2f0'); ctx.fill()
            pop_scale(ctx, 640, 365, pm, msg)
        for k, (lab, col) in enumerate(FLAGS):
            p = prog(lt, l1 + 0.6 + k * 0.45, l1 + 0.9 + k * 0.45)
            x, y = 1100 + (k % 2) * 330, 380 + (k // 2) * 160
            if p > 0:
                ctx.move_to(x - 120, y + 40); ctx.line_to(x - 120, y - 50); ctx.set_line_width(8); src(ctx, C['white'], p); ctx.stroke()
                pill(ctx, x + 10, y - 20, lab, col, C['white'] if col != C['yellow'] else C['dark'], 36, p)
        ps = eback(prog(lt, L[1][1] - 0.5, L[1][1] - 0.2))
        if ps > 0:
            ctx.save(); ctx.translate(1265, 720); ctx.scale(ps, ps); ctx.new_path()
            for i in range(8):
                aa = math.pi / 8 + i * math.pi / 4; ctx.line_to(110 * math.cos(aa), 110 * math.sin(aa))
            ctx.close_path(); src(ctx, C['red']); ctx.fill(); ctx.restore()
            rich(ctx, [('STOP', C['white'])], 1265, 720, 64 * ps, 1, pop=False)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 2: tips
    if l2 - 0.2 < lt < l3 + 0.2:
        a = prog(lt, l2 - 0.2, l2 + 0.2) * (1 - prog(lt, l3 - 0.3, l3 + 0.1))
        ctx.push_group()
        for k, (t1, t2, col, icon) in enumerate(TIPS):
            st = [l2 + 0.2, l2 + 2.0, l2 + 4.0][k]
            p = eback(prog(lt, st, st + 0.45), 1.4)
            if p <= 0: continue
            x = 160 + k * 560; y = 300 + (1 - p) * 700
            card(ctx, x, y, 480, 480, '#20307e', 46)
            glow(ctx, x + 240, y + 160, 160, col, 0.5)
            circle(ctx, x + 240, y + 160, 95, col); icon(ctx, x + 240, y + 160, 1.5)
            rich(ctx, [(t1, C['white'])], x + 240, y + 320, 52, pop=False, maxw=440)
            rich(ctx, [(t2, C['grey'])], x + 240, y + 390, 34, pop=False, w='normal', maxw=440)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 3: millions of years
    if l3 - 0.3 < lt < l4 + 0.4:
        a = prog(lt, l3 - 0.2, l3 + 0.3) * (1 - prog(lt, l4 + 0.0, l4 + 0.4))
        ctx.push_group()
        sy = lerp(900, 520, eo(prog(lt, l3, l3 + 1.5)))
        glow(ctx, 1300, sy, 400, C['yellow'], 0.7); circle(ctx, 1300, sy, 110, '#fff0b0')
        hills(ctx, 820, '#3a2a6a', amp=50, phase=0.8)
        hills(ctx, 900, '#241a4f', amp=30, phase=2.0)
        person(ctx, 640, 800, 1.6, mono='#170f33', arm_l=0.3, arm_r=1.9)
        text_left(ctx, [('millions of years', C['white'])], 150, 200, 72, prog(lt, l3 + 0.6, l3 + 0.9), pop=True)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 4: chain of trust
    if l4 - 0.2 < lt < l5 + 0.2:
        a = prog(lt, l4 - 0.1, l4 + 0.3) * (1 - prog(lt, l5 - 0.2, l5 + 0.2))
        ctx.push_group()
        nodes = [(360, 'Source', C['cyan']), (760, 'Credentials', C['yellow']), (1160, 'Publisher', C['green']),
                 (1560, 'You', C['orange'])]
        for k, (x, lab, col) in enumerate(nodes):
            p = eback(prog(lt, l4 + 0.3 + k * 0.35, l4 + 0.6 + k * 0.35))
            if k > 0:
                q = prog(lt, l4 + 0.2 + k * 0.35, l4 + 0.5 + k * 0.35)
                px = nodes[k - 1][0]
                ctx.move_to(px + 90, 560); ctx.line_to(lerp(px + 90, x - 90, q), 560); ctx.set_line_width(10)
                ctx.set_dash([20, 14], -(t * 60) % 34); src(ctx, C['white'], 0.6); ctx.stroke(); ctx.set_dash([])
            if p > 0:
                glow(ctx, x, 560, 160, col, 0.5); circle(ctx, x, 560, 80 * p, col)
                rich(ctx, [(lab, C['white'])], x, 700, 44, p, pop=False)
        title(ctx, [('Trust comes from ', C['white']), ('the source', C['cyan'])], 230, 72, prog(lt, l4 + 0.4, l4 + 0.7))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 5: final
    if lt > l5 - 0.3:
        a = prog(lt, l5 - 0.2, l5 + 0.2)
        ctx.push_group()
        bl = lt - (l5 + 1.6)
        openness = 1.0 - (math.sin(math.pi * clamp(bl / 0.26)) if 0 < bl < 0.26 else 0)
        openness *= eo(prog(lt, l5, l5 + 0.4))
        big_eye(ctx, 960, 430, 0.85, openness, math.sin(math.pi * prog(lt, l5 + 0.3, l5 + 0.7)) * 0.8, t, int(t * 30))
        title(ctx, [("Don't just trust. ", C['white']), ('VERIFY.', C['yellow'])], 800, 110, prog(lt, l5 + 0.4, l5 + 0.7))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
