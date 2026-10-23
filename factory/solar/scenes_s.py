from props import *


def starts(L): return [a for a, b in L]


# ===================================================================== 0  1859
def observatory(ctx, t, lt, l0, l1):
    # warm room
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#2a1f4f')); g.add_color_stop_rgba(1, *hexc('#4a2a5a'))
    ctx.set_source(g); ctx.paint()
    glow(ctx, 1300, 380, 900, '#ffb34a', 0.35)
    # window with sunlight beam
    rrect(ctx, 180, 140, 360, 460, 180); src(ctx, '#ffe9a8'); ctx.fill()
    ctx.move_to(180, 380); ctx.line_to(540, 380); ctx.move_to(360, 140); ctx.line_to(360, 600)
    ctx.set_line_width(12); src(ctx, '#2a1f4f'); ctx.stroke()
    ctx.move_to(380, 300); ctx.line_to(1250, 440); ctx.line_to(1250, 640); ctx.line_to(380, 420); ctx.close_path()
    ctx.set_source_rgba(1, 0.95, 0.7, 0.10); ctx.fill()
    # floor
    ctx.rectangle(0, 820, W, 300); src(ctx, '#3a2a5a'); ctx.fill()
    # telescope on tripod
    ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, '#8c6a45')
    ctx.move_to(700, 820); ctx.line_to(760, 560); ctx.line_to(820, 820); ctx.move_to(760, 560); ctx.line_to(760, 820); ctx.stroke()
    ctx.save(); ctx.translate(760, 540); ctx.rotate(-0.35)
    rrect(ctx, -260, -34, 520, 68, 30); src(ctx, '#b0875a'); ctx.fill()
    rrect(ctx, 200, -44, 80, 88, 20); src(ctx, '#8c6a45'); ctx.fill(); ctx.restore()
    # projection screen with the sun
    rrect(ctx, 1130, 380, 300, 320, 16); src(ctx, '#f4efe6'); ctx.fill()
    ctx.move_to(1280, 700); ctx.line_to(1280, 820); ctx.set_line_width(12); src(ctx, '#8c6a45'); ctx.stroke()
    flare = math.sin(math.pi * prog(lt, l1 + 0.1, l1 + 2.4)) if lt > l1 else 0
    ctx.save(); ctx.new_path(); ctx.arc(1280, 540, 120, 0, 2 * math.pi); ctx.clip()
    circle(ctx, 1280, 540, 120, '#ffe0a0')
    for (sx, sy, sr) in SPOTS: circle(ctx, 1280 + sx * 120, 540 + sy * 120, sr * 120, '#3a2a1a', 0.85)
    if flare > 0:
        for ox, oy in ((0.33, -0.25), (0.42, -0.17)):
            glow(ctx, 1280 + ox * 120, 540 + oy * 120, 50 * (0.5 + flare), '#ffffff', flare)
            circle(ctx, 1280 + ox * 120, 540 + oy * 120, 8 * (0.5 + flare), '#ffffff', flare)
    ctx.restore()
    # Carrington (top hat) sketching
    px = 1010
    person(ctx, px, 820, 1.7, shirt='#3a3f6a', arm_l=0.3, arm_r=1.1 + 0.08 * math.sin(t * 12) * (lt < l1),
           hair='#3a2a1a')
    rrect(ctx, px - 46, 820 - 1.7 * 230 - 70, 92, 80, 8); src(ctx, '#151032'); ctx.fill()
    rrect(ctx, px - 70, 820 - 1.7 * 230 + 4, 140, 14, 7); src(ctx, '#151032'); ctx.fill()
    # sketch pad
    rrect(ctx, px + 70, 560, 90, 120, 6); src(ctx, '#f4efe6'); ctx.fill()
    for (sx, sy, sr) in SPOTS[:3]: circle(ctx, px + 115 + sx * 40, 620 + sy * 40, 5, '#3a2a1a')


def s0(ctx, lt, t, L):
    l0, l1, l2, l3, l4, l5 = starts(L)
    if lt < l2 + 0.3:
        observatory(ctx, t, lt, l0, l1)
        pill(ctx, 260, 80, 'England · 1 September 1859', C['yellow'], C['dark'], 34, prog(lt, 0.4, 0.8))
        rich(ctx, [('Richard Carrington', C['white'])], 1010, 230, 44, prog(lt, l0 + 2.0, l0 + 2.4))
        fl = prog(lt, l1 + 0.5, l1 + 0.75) * (1 - prog(lt, l1 + 0.9, l1 + 1.6))
        if fl > 0: ctx.set_source_rgba(1, 1, 1, 0.85 * fl); ctx.paint()
        if lt < l2 - 0.3: return
    # ---- line 2: auroras across the globe
    def globe_scene():
        bg(ctx, t, top='#050a26', bot='#10184a', glow_col='#1f5a6a', gy=540)
        earth(ctx, 960, 560, 330, t)
        sp = eo(prog(lt, l2 + 0.2, l2 + 2.6))
        ctx.save(); ctx.new_path(); ctx.arc(960, 560, 330, 0, 2 * math.pi); ctx.clip()
        band = lerp(120, 300, sp)
        g = cairo.LinearGradient(0, 560 - 330, 0, 560 - 330 + band * 1.4)
        g.add_color_stop_rgba(0, 0.37, 0.89, 0.54, 0.75); g.add_color_stop_rgba(0.6, 0.24, 0.88, 1.0, 0.45)
        g.add_color_stop_rgba(1, 1.0, 0.3, 0.5, 0.0)
        ctx.rectangle(560, 220, 800, band * 1.4); ctx.set_source(g); ctx.fill()
        ctx.restore()
        for k, (nm, x, y) in enumerate((('Hawaii', 760, 600), ('Cuba', 1030, 560), ('Colombia', 1080, 660))):
            p = eback(prog(lt, l2 + 2.2 + k * 0.45, l2 + 2.5 + k * 0.45))
            if p > 0:
                circle(ctx, x, y, 12 * p, C['pink']); glow(ctx, x, y, 50, C['pink'], 0.6 * p)
                pill(ctx, x + (0 if k else -40), y - 50, nm, C['white'], C['dark'], 30, p)
        title(ctx, [('The sky caught fire', C['green'])], 120, 70, prog(lt, l2 + 0.5, l2 + 0.9))
    if lt < l3 + 0.3:
        a = prog(lt, l2 - 0.3, l2 + 0.2) * (1 - prog(lt, l3 - 0.2, l3 + 0.3)) if lt > l2 - 0.3 else 0
        ctx.push_group(); globe_scene(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        if lt < l3 - 0.2: return
    # ---- line 3: telegraph office
    def tele():
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#14103a')); g.add_color_stop_rgba(1, *hexc('#2a1f4f'))
        ctx.set_source(g); ctx.paint()
        aurora(ctx, 0, W, 40, 420, t, 0.7)
        # window frame
        ctx.rectangle(0, 0, W, H); ctx.rectangle(220, 60, 1480, 440); ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        src(ctx, '#2a1f4f'); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
        ctx.rectangle(0, 800, W, 300); src(ctx, '#3a2a5a'); ctx.fill()
        rrect(ctx, 520, 640, 900, 30, 12); src(ctx, '#8c6a45'); ctx.fill()
        for lx in (560, 1360): ctx.rectangle(lx, 660, 22, 160); src(ctx, '#6b4f33'); ctx.fill()
        press = 1.0 if math.sin(t * 14) > 0.3 else 0.0
        telegraph(ctx, 960, 620, 1.2, t, press)
        # wires overhead
        wire_line(ctx, [(0, 520), (480, 540), (960, 520), (1440, 540), (W, 520)], t, 1, current=1.0, col='#9aaad6')
        shock = l3 + 0.8 < lt < l3 + 3.0
        for k, x in enumerate((480, 960, 1440)):
            if math.sin(t * 9 + k * 2) > 0.2: spark(ctx, x, 540, 60, t, 1, seed=k)
        person(ctx, 760, 800, 1.6, shirt='#5a3f6a', arm_l=2.6 if shock else 0.3, arm_r=2.6 if shock else 1.1,
               rot=0.05 * math.sin(t * 50) * shock)
        if shock:
            bolt(ctx, 700, 330, 0.8); bolt(ctx, 830, 350, 0.7)
        pb = prog(lt, l3 + 3.4, l3 + 3.8)
        if pb > 0:
            def batt():
                rrect(ctx, 1500, 600, 180, 110, 14); src(ctx, '#6b7fb8'); ctx.fill()
                rrect(ctx, 1530, 585, 30, 20, 4); ctx.fill(); rrect(ctx, 1620, 585, 30, 20, 4); ctx.fill()
                rich(ctx, [('+  −', C['white'])], 1590, 655, 50, pop=False, shadow=False)
            pop_scale(ctx, 1590, 650, pb, batt)
            x_mark(ctx, 1590, 650, 70, prog(lt, l3 + 3.9, l3 + 4.3))
            pill(ctx, 1590, 500, 'unplugged', C['red'], C['white'], 30, prog(lt, l3 + 4.0, l3 + 4.3))
            pm = prog(lt, l3 + 4.6, L[3][1])
            if pm > 0:
                for k in range(12):
                    u = (lt * 0.6 + k / 12) % 1
                    x = lerp(980, 1900, u)
                    if k % 3 == 0: rrect(ctx, x, 440, 40, 12, 6)
                    else: ctx.new_path(); ctx.arc(x + 6, 446, 7, 0, 2 * math.pi)
                    src(ctx, C['cyan'], pm * (1 - u) * 0.9); ctx.fill()
                rich(ctx, [('...still sending', C['cyan'])], 1450, 400, 40, pm, w='normal')
    if lt < l4 + 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3) * (1 - prog(lt, l4 - 0.2, l4 + 0.3))
        ctx.push_group(); tele(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        if lt < l4 - 0.2: return
    # ---- line 4: then vs now
    def split():
        bg(ctx, t, glow_col='#4a2a9a', gy=560)
        sp = ss(prog(lt, l4, l4 + 0.6))
        # left 1859
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#3a2a4a')); g.add_color_stop_rgba(1, *hexc('#5a3a4a'))
        ctx.set_source(g); ctx.paint()
        telegraph(ctx, 480, 640, 1.3, t)
        rich(ctx, [('1859', C['yellow'])], 480, 260, 110, sp)
        rich(ctx, [('a curiosity', C['white'])], 480, 820, 54, prog(lt, l4 + 0.8, l4 + 1.1))
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        bg(ctx, t, top='#070c2c', bot='#1a1f5a', glow_col='#3a2a8a', gx=1440, gy=600)
        city(ctx, 760, t, 1.0, seed=9, x0=960, x1=W)
        for k, (x, y) in enumerate(((1250, 230), (1640, 180))): satellite(ctx, x, y, 1.0, 0.3 * math.sin(t + k))
        pylon(ctx, 1500, 760, 1.2)
        rich(ctx, [('TODAY', C['cyan'])], 1440, 380, 110, sp)
        rich(ctx, [('a catastrophe', C['red'])], 1440, 860, 54, prog(lt, l4 + 2.0, l4 + 2.3))
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    if lt < l5 + 0.3:
        a = prog(lt, l4 - 0.2, l4 + 0.3) * (1 - prog(lt, l5 - 0.2, l5 + 0.3))
        ctx.push_group(); split(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        if lt < l5 - 0.2: return
    # ---- line 5: title
    a = prog(lt, l5 - 0.2, l5 + 0.3)
    ctx.push_group()
    bg(ctx, t, top='#05061a', bot='#140c2e', glow_col='#5a2a1a', gx=200, gy=540)
    sun(ctx, -120, 540, 520, t, flare=0.6 + 0.4 * math.sin(t * 3), loops=1)
    cme(ctx, 380, 540, prog(lt, l5 + 0.4, L[5][1] + 2.5), 1300, 0.0, 0.5, 0.9)
    earth(ctx, 1700, 560, 110, t, night=0.4)
    magnetosphere(ctx, 1700, 560, 110, t, squeeze=0.3 * prog(lt, L[5][1], L[5][1] + 2), a=0.8)
    te = L[5][1]
    rich(ctx, [('WHAT IF A', C['white'])], 1060, 380, 80, prog(lt, te + 0.0, te + 0.35), maxw=1100)
    rich(ctx, [('SOLAR SUPERSTORM', C['yellow'])], 1060, 500, 110, prog(lt, te + 0.2, te + 0.55), maxw=1150)
    rich(ctx, [('HIT EARTH TODAY?', C['white'])], 1060, 620, 92, prog(lt, te + 0.4, te + 0.75), maxw=1100)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ===================================================================== 1  HOW THE SUN ATTACKS
def s1(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#05061a', bot='#140c2e', glow_col='#5a2a1a', gx=300, gy=540)
    if lt < l2 + 0.3:
        a = 1 - prog(lt, l2 - 0.2, l2 + 0.3)
        ctx.push_group()
        zoom = lerp(1.25, 1.0, eo(prog(lt, 0, 2.5)))
        ctx.save(); ctx.translate(560, 540); ctx.scale(zoom, zoom); ctx.translate(-560, -540)
        snap = prog(lt, l1 + 1.0, l1 + 1.4)
        sun(ctx, 420, 560, 420, t, flare=snap * (1 - prog(lt, l1 + 1.6, l1 + 3.5)), loops=1)
        # twisting field lines
        for k in range(4):
            ph = t * 0.6 + k
            ctx.new_path()
            for i in range(41):
                u = i / 40; ang = -0.9 + 1.8 * u
                rr = 420 + 160 * math.sin(math.pi * u) * (0.8 + 0.2 * math.sin(ph)) + 30 * k
                x = 420 + rr * math.cos(ang); y = 560 + rr * math.sin(ang) * 0.9
                if snap > 0 and k == 1 and 0.4 < u < 0.6: continue
                (ctx.move_to if i == 0 or (snap > 0 and k == 1 and abs(u - 0.62) < 0.03) else ctx.line_to)(x, y)
            ctx.set_line_width(5); src(ctx, C['pink'] if k == 1 else '#ffb34a', 0.7 if k == 1 else 0.4); ctx.stroke()
        ctx.restore()
        text_left(ctx, [('plasma', C['yellow'])], 1150, 380, 72, prog(lt, l0 + 1.8, l0 + 2.1), pop=True)
        text_left(ctx, [('+ magnetic fields', C['pink'])], 1150, 470, 64, prog(lt, l0 + 2.6, l0 + 2.9), pop=True)
        cme(ctx, 820, 520, prog(lt, l1 + 1.1, l1 + 4.5), 1300, -0.05, 0.6, 1.0)
        if lt > l1:
            text_left(ctx, [('Coronal Mass Ejection', C['white'])], 1100, 700, 56, prog(lt, l1 + 2.2, l1 + 2.5))
            text_left(ctx, [('billions of tons of charged gas', C['grey'])], 1100, 770, 40, prog(lt, l1 + 3.0, l1 + 3.3), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 2: distance & 17 hours
    if l2 - 0.3 < lt < l3 + 0.3:
        a = prog(lt, l2 - 0.2, l2 + 0.3) * (1 - prog(lt, l3 - 0.2, l3 + 0.3))
        ctx.push_group()
        sun(ctx, 140, 540, 220, t, loops=0.6)
        earth(ctx, 1720, 540, 70, t)
        ctx.move_to(380, 540); ctx.line_to(1630, 540); ctx.set_dash([18, 16]); ctx.set_line_width(4); src(ctx, C['grey'], 0.6)
        ctx.stroke(); ctx.set_dash([])
        rich(ctx, [('150 million km', C['white'])], 1000, 480, 50, prog(lt, l2 + 0.8, l2 + 1.1))
        p = prog(lt, l2 + 2.0, l2 + 4.8)
        cme(ctx, 360, 540, p, 1300, 0, 0.35, 1.0)
        hrs = 17 * p
        rich(ctx, [('Most miss us', C['grey'])], 1000, 760, 42, prog(lt, l2 + 0.2, l2 + 0.5) * (1 - prog(lt, l2 + 1.6, l2 + 1.9)), w='normal')
        if p > 0:
            rich(ctx, [(f'{hrs:4.1f} hours', C['yellow'])], 1000, 720, 96, prog(lt, l2 + 2.0, l2 + 2.3), pop=False)
            rich(ctx, [('Carrington, 1859', C['grey'])], 1000, 810, 40, prog(lt, l2 + 2.2, l2 + 2.5), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 3: magnetosphere shake -> currents
    if lt > l3 - 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3)
        ctx.push_group()
        bg(ctx, t, glow_col='#1f3a7a', gy=540)
        zz = ss(prog(lt, l3 + 2.6, l3 + 3.4))
        ex = lerp(760, 1500, zz); er = lerp(200, 90, zz)
        sq = 0.5 + 0.2 * math.sin(t * 6)
        cme(ctx, -100, 540, 1.0, ex - 160, 0, 0.6, 0.6 * (1 - zz))
        magnetosphere(ctx, ex, 540, er, t, squeeze=sq * (1 - zz * 0.5), shake=1.0, a=1 - 0.4 * zz)
        earth(ctx, ex, 540, er, t)
        if zz > 0:
            ctx.push_group()
            ctx.rectangle(0, 700, 1250, 380); src(ctx, '#1d2c6e'); ctx.fill()
            pts = [(-40, 560), (300, 570), (640, 560), (980, 570), (1300, 560)]
            for x, y in pts[1:-1]: pylon(ctx, x, 720, 0.9)
            wire_line(ctx, [(x, 525) for x, y in pts], t, 1, current=1.0, pulse_col=C['yellow'])
            # pipeline
            rrect(ctx, -20, 840, 1300, 40, 20); src(ctx, '#6b7fb8'); ctx.fill()
            for k in range(6):
                u = (t * 0.5 + k / 6) % 1
                glow(ctx, u * 1260, 860, 40, C['yellow'], 0.7)
            labels = [('power lines', 160, 430), ('pipelines', 160, 800), ('cables', 160, 960)]
            ctx.rectangle(-20, 950, 1300, 14); src(ctx, '#9aaad6'); ctx.fill()
            for k in range(8):
                u = (t * 0.7 + k / 8) % 1; circle(ctx, u * 1260, 957, 6, C['yellow'])
            for k, (lb, x, y) in enumerate(labels):
                pill(ctx, x, y, lb, C['yellow'], C['dark'], 30, prog(lt, l3 + 3.6 + k * 0.4, l3 + 3.9 + k * 0.4))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(zz)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ===================================================================== 2  WARNING SHOTS
def s2(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = starts(L)
    if lt < l1 + 0.3:
        bg(ctx, t, glow_col='#3a2a8a', gy=560)
        title(ctx, [('Warning shots', C['yellow'])], 300, 110, prog(lt, 0.2, 0.6))
        for k, (yr, col) in enumerate(((1989, C['cyan']), (2022, C['pink']), (2024, C['green']))):
            p = eback(prog(lt, 0.8 + k * 0.3, 1.2 + k * 0.3))
            x = 560 + k * 400
            if p > 0:
                ctx.save(); ctx.translate(x, 620); ctx.scale(p, p)
                circle(ctx, 0, 0, 110, col); rich(ctx, [(str(yr), C['dark'])], 0, 0, 56, pop=False, shadow=False)
                ctx.restore()
        ctx.move_to(450, 620); ctx.line_to(1470, 620)
        if lt > l1 - 0.3:
            pass
        if lt < l1 - 0.2: return
    # ---- line 1: Quebec
    if l1 - 0.3 < lt < l2 + 0.3:
        a = prog(lt, l1 - 0.2, l1 + 0.3) * (1 - prog(lt, l2 - 0.2, l2 + 0.3))
        ctx.push_group()
        out = prog(lt, l1 + 2.4, l1 + 3.4)
        bg(ctx, t, top=lerp_col('#1a2a6e', '#05061a', out), bot=lerp_col('#3a4a9a', '#10184a', out), glow_col='#3d5ab8', gy=700,
           stars=0.4 + 0.6 * out)
        aurora(ctx, 0, W, 60, 420, t, 0.6)
        hills(ctx, 780, '#d8e2ff', amp=30, phase=0.6)
        hills(ctx, 880, '#b8c6f0', amp=24, phase=2.1)
        pts = [(-40, 0), (380, 0), (820, 0), (1260, 0), (1700, 0), (2000, 0)]
        for x, _ in pts[1:-1]: pylon(ctx, x, 800, 1.0)
        wire_line(ctx, [(x, 560) for x, _ in pts], t, 1, current=1.0 - out)
        rnd = random.Random(4)
        for k in range(16):
            x = 80 + k * 115 + rnd.uniform(-20, 20); y = 900 + rnd.uniform(-20, 30)
            house(ctx, x, y, 0.75, rnd.choice(['#ff8a3d', '#ffd23f', '#3ee0ff', '#ff4f81']), lit=(out < 0.5 + k * 0.03))
        tm = prog(lt, l1 + 1.0, l1 + 2.6)
        if tm > 0 and out < 1:
            ring_timer(ctx, 1640, 260, 90, 1 - tm, f'{int(90 * (1 - tm))}s', 1 - out)
        title(ctx, [('Québec · March 1989', C['white'])], 120, 64, prog(lt, l1 + 0.2, l1 + 0.5))
        if out > 0.5:
            rich(ctx, [('9 hours', C['yellow'])], 1640, 260, 90, prog(lt, l1 + 3.4, l1 + 3.7))
            rich(ctx, [('in the dark', C['grey'])], 1640, 340, 40, prog(lt, l1 + 3.6, l1 + 3.9), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 2: Starlink
    if l2 - 0.3 < lt < l3 + 0.3:
        a = prog(lt, l2 - 0.2, l2 + 0.3) * (1 - prog(lt, l3 - 0.2, l3 + 0.3))
        ctx.push_group()
        bg(ctx, t, top='#03051a', bot='#0b1640', glow_col='#1f3a7a', gy=1200)
        ctx.new_path(); ctx.arc(960, 2600, 1800, 0, 2 * math.pi); src(ctx, '#2d6be0'); ctx.fill()
        puff = prog(lt, l2 + 2.2, l2 + 3.2)
        for k in range(4):
            ctx.new_path(); ctx.arc(960, 2600, 1800 + 30 + k * (40 + 90 * puff), 0, 2 * math.pi); ctx.set_line_width(40 + 30 * puff)
            src(ctx, C['cyan'], (0.12 - 0.025 * k) * (1 + 1.5 * puff)); ctx.stroke()
        for k in range(14):
            u = k / 13
            x = 300 + u * 1300
            base_y = 470 + 120 * (u - 0.5) ** 2 * 4
            fall = prog(lt, l2 + 3.2 + k * 0.08, l2 + 5.0 + k * 0.08)
            y = base_y + 420 * fall ** 1.5
            if fall > 0:
                ctx.move_to(x, y); ctx.line_to(x - 40, y - 120 * fall); ctx.set_line_width(10); src(ctx, C['orange'], 0.6 * fall)
                ctx.stroke()
                glow(ctx, x, y, 40, C['orange'], 0.7 * fall)
            satellite(ctx, x, y, 0.55, 0.5 * fall, a=1 - 0.6 * fall, glitch_=fall)
        title(ctx, [('Starlink · February 2022', C['white'])], 120, 64, prog(lt, l2 + 0.2, l2 + 0.5))
        rich(ctx, [('~40', C['orange'])], 1650, 280, 120, prog(lt, l2 + 3.6, l2 + 3.9))
        rich(ctx, [('satellites lost', C['grey'])], 1650, 370, 40, prog(lt, l2 + 3.8, l2 + 4.1), w='normal')
        pill(ctx, 960, 760, 'upper atmosphere puffs up', C['cyan'], C['dark'], 32, prog(lt, l2 + 2.3, l2 + 2.6))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 3: tractors
    if l3 - 0.3 < lt < l4 + 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3) * (1 - prog(lt, l4 - 0.2, l4 + 0.3))
        ctx.push_group()
        bg(ctx, t, top='#2a3a8a', bot='#6a5aa8', glow_col='#ff8a5a', gy=800, stars=0.3)
        aurora(ctx, 0, W, 40, 380, t, 0.7, cols=('#ff4f81', '#b28cff', '#5ee38a'))
        ctx.rectangle(0, 600, W, 480); src(ctx, '#3a6a3a'); ctx.fill()
        for k in range(12):
            y = 620 + k * 36
            ctx.move_to(0, y); ctx.line_to(W, y + 20); ctx.set_line_width(8); src(ctx, '#2f5a2f'); ctx.stroke()
        p = prog(lt, l3 + 0.5, L[3][1])
        path = []
        for i in range(101):
            u = i / 100 * p
            if u < 0.4: x, y = 200 + u / 0.4 * 700, 760
            else:
                k = (u - 0.4) / 0.6; ang = k * 5.0
                x, y = 900 + 200 * math.sin(ang) + k * 350, 760 - 150 * (1 - math.cos(ang)) + k * 60
            path.append((x, y))
        ctx.new_path(); [(ctx.move_to if i == 0 else ctx.line_to)(*pp) for i, pp in enumerate(path)]
        ctx.set_line_width(14); ctx.set_dash([24, 16]); src(ctx, '#7a4a2a', 0.8); ctx.stroke(); ctx.set_dash([])
        if len(path) > 2:
            (x0, y0), (x1, y1) = path[-3], path[-1]
            tractor(ctx, x1, y1, 1.2, math.atan2(y1 - y0, x1 - x0) * 0.5)
            if p > 0.45:
                ctx.save(); ctx.translate(x1, y1 - 200)
                circle(ctx, 0, 0, 36, C['red']); circle(ctx, 0, -2, 14, C['white']); ctx.restore()
                rich(ctx, [('?', C['yellow'])], x1 + 60, y1 - 210, 80, 1)
        title(ctx, [('May 2024 · strongest storm in 20 years', C['white'])], 120, 58, prog(lt, l3 + 0.2, l3 + 0.5))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- line 4: scale comparison
    if lt > l4 - 0.3:
        a = prog(lt, l4 - 0.2, l4 + 0.3)
        ctx.push_group()
        bg(ctx, t, glow_col='#5a2a1a', gy=700)
        for k, (lab, hh, col) in enumerate((('1989', 0.33, C['cyan']), ('2022', 0.08, C['pink']), ('2024', 0.25, C['green']),
                                             ('Carrington', 1.0, C['orange']))):
            x = 380 + k * 380
            p = eo(prog(lt, l4 + 0.2 + k * 0.25, l4 + 0.9 + k * 0.25)) if k < 3 else eo(prog(lt, l4 + 1.2, l4 + 2.2))
            h = 620 * hh * p
            ctx.new_path(); ctx.move_to(x - 140, 860)
            for i in range(41):
                u = i / 40
                ctx.line_to(x - 140 + 280 * u, 860 - h * math.sin(math.pi * u) ** 1.5 * (1 + 0.04 * math.sin(t * 4 + u * 9)))
            ctx.line_to(x + 140, 860); ctx.close_path(); src(ctx, col, 0.9); ctx.fill()
            rich(ctx, [(lab, C['white'])], x, 910, 40, prog(lt, l4 + 0.1, l4 + 0.4), pop=False)
        rich(ctx, [('(illustrative scale)', C['grey'])], 960, 200, 30, prog(lt, l4 + 1.4, l4 + 1.7), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ===================================================================== 3  DAY ZERO TIMELINE
STEPS = [('DAY 0', 'flare'), ('+8 min', 'light'), ('+hours', 'particles'), ('~1 day', 'CME impact')]


def timeline_bar(ctx, lt, marks, active, a=1.0):
    ctx.move_to(260, 110); ctx.line_to(1660, 110); ctx.set_line_width(6); ctx.set_source_rgba(1, 1, 1, 0.25 * a); ctx.stroke()
    for k, (lab, sub) in enumerate(STEPS):
        x = 260 + k * 466
        on = k <= active
        circle(ctx, x, 110, 16, C['yellow'] if on else '#3a4a9a', a)
        rich(ctx, [(lab, C['white'] if on else C['grey'])], x, 160, 34, a, pop=False)


def s3(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = starts(L)
    active = 0 if lt < l1 else 1 if lt < l2 else 2 if lt < l3 else 3
    bg(ctx, t, top='#05061a', bot='#10184a', glow_col='#2a1f5a', gy=600)
    # ---- 0-1: flare + light
    if lt < l2 + 0.3:
        a = 1 - prog(lt, l2 - 0.2, l2 + 0.3)
        ctx.push_group()
        fl = prog(lt, l0 + 1.6, l0 + 2.0) * (1 - 0.5 * prog(lt, l0 + 2.5, l1 + 2))
        sun(ctx, 200, 600, 330, t, flare=fl, flare_pos=(0.55, -0.2))
        if lt > l0 + 1.7 and lt < l0 + 2.0:
            ctx.set_source_rgba(1, 1, 1, 0.6 * (1 - prog(lt, l0 + 1.7, l0 + 2.0))); ctx.paint()
        earth(ctx, 1560, 620, 220, t, night=1.0)
        pb = prog(lt, l1, l1 + 1.2)
        if pb > 0:
            g = cairo.LinearGradient(400, 0, 1360, 0)
            g.add_color_stop_rgba(0, 1, 1, 1, 0.6); g.add_color_stop_rgba(1, 1, 1, 1, 0.15)
            ctx.move_to(420, 520); ctx.line_to(lerp(420, 1360, pb), 420); ctx.line_to(lerp(420, 1360, pb), 820); ctx.line_to(420, 680)
            ctx.close_path(); ctx.set_source(g); ctx.fill()
            rich(ctx, [('8 minutes', C['white'])], 880, 900, 60, prog(lt, l1 + 0.4, l1 + 0.7))
        if lt > l1 + 1.3:
            for k, ang in enumerate((-2.3, -2.9, 2.5)):
                x = 1560 + 260 * math.cos(ang); y = 620 + 260 * math.sin(ang)
                p = eback(prog(lt, l1 + 1.4 + k * 0.2, l1 + 1.7 + k * 0.2))
                if p > 0:
                    def radio(x=x, y=y):
                        circle(ctx, x, y, 44, C['white'])
                        ctx.new_path(); ctx.arc(x, y, 20, -2.4, -0.74); ctx.set_line_width(6); src(ctx, C['dark']); ctx.stroke()
                        circle(ctx, x, y + 6, 7, C['dark'])
                    pop_scale(ctx, x, y, p, radio)
                    x_mark(ctx, x, y, 30, prog(lt, l1 + 1.9 + k * 0.2, l1 + 2.2 + k * 0.2))
            rich(ctx, [('radio blackout', C['red'])], 1560, 920, 44, prog(lt, l1 + 2.0, l1 + 2.3))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- 2: particles: satellites, GPS, planes
    if l2 - 0.3 < lt < l3 + 0.3:
        a = prog(lt, l2 - 0.2, l2 + 0.3) * (1 - prog(lt, l3 - 0.2, l3 + 0.3))
        ctx.push_group()
        earth(ctx, 960, 620, 260, t)
        for k in range(90):
            u = (t * 0.25 + k * 0.618) % 1
            x = lerp(-100, 900, u); y = 620 + 400 * math.sin(k * 2.3)
            circle(ctx, x, y, 4, C['yellow'], 0.6)
        for k in range(6):
            ang = t * 0.25 + k * 1.047
            x = 960 + 420 * math.cos(ang); y = 620 + 190 * math.sin(ang)
            g = 1.0 if (lt > l2 + 1.0 and (k + int(t * 3)) % 3 == 0) else 0.0
            satellite(ctx, x, y, 0.6, ang, glitch_=g, t=t)
        pg = eback(prog(lt, l2 + 2.2, l2 + 2.6))
        if pg > 0:
            ctx.save(); ctx.translate(1520, 360); ctx.scale(pg, pg)
            ctx.move_to(0, 60); ctx.curve_to(-60, -10, -50, -70, 0, -70); ctx.curve_to(50, -70, 60, -10, 0, 60)
            src(ctx, C['red']); ctx.fill(); circle(ctx, 0, -28, 20, C['white']); ctx.restore()
            rich(ctx, [('?', C['yellow'])], 1590 + 6 * math.sin(t * 7), 300, 80, pg)
        pp = prog(lt, l2 + 3.6, L[2][1])
        if pp > 0:
            ctx.new_path(); ctx.move_to(520, 380)
            ctx.curve_to(700, lerp(200, 330, pp), 1200, lerp(200, 330, pp), 1400, 380)
            ctx.set_line_width(6); ctx.set_dash([16, 12]); src(ctx, C['white'], 0.7); ctx.stroke(); ctx.set_dash([])
            u = pp
            px = lerp(520, 1400, u); py = 380 - math.sin(math.pi * u) * lerp(150, 50, pp)
            plane(ctx, px, py, 0.8, 0.0)
            pill(ctx, 960, 180 + 60, 'rerouted away from the poles', C['white'], C['dark'], 30, prog(lt, l2 + 4.0, l2 + 4.3))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- 3: grid & transformers
    if l3 - 0.3 < lt < l4 + 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3) * (1 - prog(lt, l4 - 0.2, l4 + 0.3))
        ctx.push_group()
        hills(ctx, 820, '#1d2c6e', amp=30)
        pts = [(-40, 0), (300, 0), (640, 0)]
        for x, _ in pts[1:]: pylon(ctx, x, 820, 1.0)
        surge = prog(lt, l3 + 0.8, l3 + 2.0)
        wire_line(ctx, [(x, 580) for x, _ in pts] + [(1000, 640)], t, 1, current=surge, pulse_col=C['red'])
        heat = prog(lt, l3 + 3.0, L[3][1])
        transformer(ctx, 1180, 820, 1.5, heat, t)
        # thermometer
        ctx.save(); ctx.translate(1580, 760)
        rrect(ctx, -26, -360, 52, 360, 26); src(ctx, C['white'], 0.9); ctx.fill()
        hh = 40 + 300 * heat
        rrect(ctx, -14, -hh, 28, hh, 14); src(ctx, lerp_col('#3ee0ff', '#ff4757', heat)); ctx.fill()
        circle(ctx, 0, 0, 44, lerp_col('#3ee0ff', '#ff4757', heat)); ctx.restore()
        if heat > 0.5 and math.sin(t * 20) > 0: spark(ctx, 1180, 560, 70, t, 1)
        rich(ctx, [('transformers', C['white'])], 1180, 350, 54, prog(lt, l3 + 2.6, l3 + 2.9))
        rich(ctx, [('the hearts of the grid', C['grey'])], 1180, 420, 38, prog(lt, l3 + 3.2, l3 + 3.5), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    # ---- 4: blackout + lead time
    if lt > l4 - 0.3:
        a = prog(lt, l4 - 0.2, l4 + 0.3)
        ctx.push_group()
        wave = lerp(-200, 2200, prog(lt, l4 + 0.4, l4 + 3.0))
        city(ctx, 820, t, 1.0, seed=12, dark_wave=wave)
        ctx.set_source_rgba(0, 0, 0.05, 0.4 * prog(lt, l4 + 0.4, l4 + 3.0)); ctx.paint()
        pc = eback(prog(lt, l4 + 3.6, l4 + 4.0))
        if pc > 0:
            def crate():
                card(ctx, 660, 300, 600, 330, '#f4f6ff', 30, stroke=False)
                rich(ctx, [('ORDER: 1 transformer', C['dark'])], 960, 370, 40, pop=False, shadow=False)
                rich(ctx, [('delivery: ', '#6b7fb8'), ('2+ years', C['red'])], 960, 450, 56, pop=False, shadow=False)
                for k in range(24):
                    x = 700 + (k % 12) * 44; y = 520 + (k // 12) * 40
                    rrect(ctx, x, y, 34, 30, 6); src(ctx, '#c9d2f0' if k > 24 * prog(lt, l4 + 4.2, L[4][1]) else C['orange']); ctx.fill()
            pop_scale(ctx, 960, 465, pc, crate)
        source_line(ctx, 'Lead time: Wood Mackenzie survey, 2025', prog(lt, l4 + 4.0, l4 + 4.4))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    timeline_bar(ctx, lt, STEPS, active)


# ===================================================================== 4  LIFE WITHOUT POWER
def s4(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#03051a', bot='#0b1240', glow_col='#1f2a6a', gy=600, stars=0.8)
    if lt < l2 + 0.3:
        a = 1 - prog(lt, l2 - 0.2, l2 + 0.3)
        ctx.push_group()
        items = [(icon_tap, 'water', C['cyan'], l0 + 0.3), (icon_fuel, 'fuel', C['orange'], l0 + 1.2),
                 (icon_card, 'payments', C['yellow'], l1 + 0.1), (lambda c, x, y, s: icon_tower(c, x, y, s, t), 'phones', C['green'], l1 + 0.9),
                 (icon_med, 'medicine', C['pink'], l1 + 1.9)]
        for k, (fn, lab, col, st) in enumerate(items):
            p = eback(prog(lt, st, st + 0.4))
            if p <= 0: continue
            x = 300 + k * 330; y = 470
            ctx.save(); ctx.translate(x, y); ctx.scale(p, p); ctx.translate(-x, -y)
            circle(ctx, x, y, 120, '#20307e'); glow(ctx, x, y, 160, col, 0.35)
            fn(ctx, x, y, 1.3)
            ctx.restore()
            rich(ctx, [(lab, C['white'])], x, 650, 40, p, pop=False)
            x_mark(ctx, x + 90, y - 90, 26, prog(lt, st + 0.6, st + 0.9))
            ctx.move_to(x, 700); ctx.line_to(x, 780); ctx.line_to(960, 780); ctx.set_line_width(5); src(ctx, C['grey'], 0.4 * p); ctx.stroke()
        pg = prog(lt, l1 + 2.6, l1 + 3.0)
        if pg > 0:
            def plug():
                rrect(ctx, 900, 780, 120, 90, 18); src(ctx, '#6b7fb8'); ctx.fill()
                for sx in (-1, 1): rrect(ctx, 960 + sx * 25 - 6, 870, 12, 30, 4); src(ctx, '#d4dcf2'); ctx.fill()
                rich(ctx, [('grid', C['white'])], 960, 825, 34, pop=False, shadow=False)
            pop_scale(ctx, 960, 825, pg, plug)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    if l2 - 0.3 < lt < l3 + 0.3:
        a = prog(lt, l2 - 0.2, l2 + 0.3) * (1 - prog(lt, l3 - 0.2, l3 + 0.3))
        ctx.push_group()
        title(ctx, [("Lloyd's of London estimate", C['grey'])], 120, 44, prog(lt, l2 + 0.2, l2 + 0.5), w='normal')
        n_on = prog(lt, l2 + 1.4, l2 + 3.0)
        for k in range(60):
            r_, c_ = divmod(k, 15)
            x = 360 + c_ * 86; y = 300 + r_ * 130
            dark = k / 60 < n_on
            person(ctx, x, y + 80, 0.42, shirt='#2a3a7a' if dark else C['yellow'], mono='#1a2350' if dark else None)
        rich(ctx, [('20–40 million', C['yellow'])], 960, 880, 84, prog(lt, l2 + 2.6, l2 + 2.9))
        rich(ctx, [('Americans without power · weeks to 2 years', C['white'])], 960, 960, 40, prog(lt, l2 + 3.4, l2 + 3.7), w='normal')
        source_line(ctx, "Source: Lloyd's & AER, Solar Storm Risk to the North American Electric Grid, 2013", 1)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    if lt > l3 - 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3)
        ctx.push_group()
        v = 2.6 * eo(prog(lt, l3 + 0.6, L[3][1]))
        for k in range(int(v / 2.6 * 24)):
            x = 760 + (k % 6) * 70; y = 760 - (k // 6) * 46
            money(ctx, x, y, 1.0, 0)
        rich(ctx, [(f'${v:.1f} TRILLION', C['green'])], 960, 330, 130, prog(lt, l3 + 0.4, l3 + 0.7), pop=False)
        rich(ctx, [('for the US alone (upper estimate)', C['grey'])], 960, 430, 40, prog(lt, l3 + 0.8, l3 + 1.1), w='normal')
        source_line(ctx, "Source: Lloyd's & AER, 2013", 1)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ===================================================================== 5  THE NEAR MISS
def s5(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#03051a', bot='#140c2e', glow_col='#3a1a3a', gy=540)
    if lt < l1 + 0.3:
        a = 1 - prog(lt, l1 - 0.2, l1 + 0.3)
        title(ctx, [('It almost happened.', C['white'])], 540, 110, prog(lt, 0.4, 0.8) * a)
        return
    cx, cy, R = 960, 560, 360
    a = prog(lt, l1 - 0.2, l1 + 0.3)
    ctx.push_group()
    sun(ctx, cx, cy, 70, t, loops=0.5, glow_a=0.6)
    ctx.new_path(); ctx.arc(cx, cy, R, 0, 2 * math.pi); ctx.set_line_width(4); ctx.set_dash([14, 12]); src(ctx, C['grey'], 0.5)
    ctx.stroke(); ctx.set_dash([])
    # earth moves counterclockwise; at hit time it is 1 week ahead
    ang_hit = -0.25
    week = 2 * math.pi * 7 / 365
    em = prog(lt, l1, l2 + 2.0)
    ea = lerp(ang_hit + 0.08, ang_hit + 0.62, em)
    ex, ey = cx + R * math.cos(ea), cy + R * math.sin(ea)
    # STEREO-A
    sa = ang_hit + 0.02
    sx, sy = cx + (R + 10) * math.cos(sa), cy + (R + 10) * math.sin(sa)
    pc = prog(lt, l1 + 0.8, l2 + 2.0)
    if pc > 0:
        for (u, v, sp, sz) in CME_P[:200]:
            d = (R + 200) * pc * sp
            w_ = v * 0.6 * d
            x = cx + d * math.cos(ang_hit) - w_ * math.sin(ang_hit); y = cy + d * math.sin(ang_hit) + w_ * math.cos(ang_hit)
            circle(ctx, x, y, sz * 0.8, '#ffb34a', 0.6)
    satellite(ctx, sx, sy, 0.45, sa, panel=C['yellow'])
    pill(ctx, sx + 150, sy - 40, 'STEREO-A', C['yellow'], C['dark'], 28, prog(lt, l2 + 2.0, l2 + 2.3))
    if pc > 0.9 and lt < l2 + 4:
        glow(ctx, sx, sy, 120, C['yellow'], 0.6 * (0.6 + 0.4 * math.sin(t * 10)))
    # trail of earth
    for k in range(20):
        a2 = ea - k * 0.02
        circle(ctx, cx + R * math.cos(a2), cy + R * math.sin(a2), 6, C['cyan'], 0.4 * (1 - k / 20))
    earth(ctx, ex, ey, 40, t)
    pill(ctx, ex + 110, ey + 30, 'Earth', C['cyan'], C['dark'], 28, 1)
    rich(ctx, [('July 23, 2012', C['yellow'])], 260, 160, 54, prog(lt, l1 + 0.3, l1 + 0.6))
    if lt > l2 + 0.5:
        m = prog(lt, l2 + 0.8, l2 + 1.4)
        ctx.new_path(); ctx.arc(cx, cy, R - 50, ang_hit, ea); ctx.set_line_width(8); src(ctx, C['pink'], m); ctx.stroke()
        mid = (ea + ang_hit) / 2
        rich(ctx, [('~1 week', C['pink'])], cx + (R - 190) * math.cos(mid), cy + (R - 190) * math.sin(mid), 40, m)
        rich(ctx, [('(not to scale)', C['grey'])], 960, 1000, 28, m, w='normal', pop=False)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a * (1 - prog(lt, l3 - 0.2, l3 + 0.3)))
    if lt > l3 - 0.3:
        a3 = prog(lt, l3 - 0.2, l3 + 0.3)
        ctx.push_group()
        p = prog(lt, l3 + 0.8, l3 + 2.2)
        ctx.new_path(); ctx.arc(960, 520, 250, 0, 2 * math.pi); ctx.set_line_width(60); ctx.set_source_rgba(1, 1, 1, 0.1); ctx.stroke()
        ctx.new_path(); ctx.arc(960, 520, 250, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.12 * p); ctx.set_line_width(60)
        src(ctx, C['red']); ctx.stroke()
        rich(ctx, [(f'{12 * p:.0f}%', C['white'])], 960, 520, 150, prog(lt, l3 + 0.6, l3 + 0.9), pop=False)
        rich(ctx, [('chance of a Carrington-class hit within a decade', C['white'])], 960, 860, 46, prog(lt, l3 + 2.0, l3 + 2.3))
        rich(ctx, [('(P. Riley, Space Weather \u00b7 via NASA Science, 2014)', C['grey'])], 960, 920, 30, prog(lt, l3 + 2.4, l3 + 2.7), w='normal')
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a3)
    source_line(ctx, 'Sources: NASA Science (2014); Baker et al., Space Weather (2013)', prog(lt, l1 + 1, l1 + 1.4))


# ===================================================================== 6  DEFENCE
def s6(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    warm = ss(prog(lt, 0.3, 2.0))
    bg(ctx, t, top=lerp_col('#05061a', '#0b1640', warm), bot=lerp_col('#140c2e', '#2a3a8a', warm), glow_col='#2a5ab8', gy=600)
    if lt < l2 + 0.3:
        a = 1 - prog(lt, l2 - 0.2, l2 + 0.3)
        ctx.push_group()
        sun(ctx, -60, 560, 300, t, loops=0.6)
        earth(ctx, 1720, 560, 100, t)
        sx = lerp(1400, 1470, 0.5 + 0.5 * math.sin(t * 0.8))
        pin = eback(prog(lt, l0 + 0.6, l0 + 1.1))
        if pin > 0:
            satellite(ctx, 1470, 560, 1.0 * pin, 0.1 * math.sin(t), panel=C['yellow'])
            pill(ctx, 1470, 450, 'solar wind monitor', C['yellow'], C['dark'], 28, pin)
            for k in range(3):
                ph = (t * 0.8 + k / 3) % 1
                ctx.new_path(); ctx.arc(1470, 560, 60 + 120 * ph, math.pi * 0.8, math.pi * 1.2)
                ctx.set_line_width(6); src(ctx, C['yellow'], 1 - ph); ctx.stroke()
        if lt > l1:
            ctx.move_to(1470, 680); ctx.line_to(1720, 680); ctx.set_line_width(4); src(ctx, C['grey'], 0.7); ctx.stroke()
            rich(ctx, [('1.5 million km', C['grey'])], 1595, 720, 30, prog(lt, l1 + 0.6, l1 + 0.9), w='normal')
            pt = prog(lt, l1 + 1.6, l1 + 2.0)
            if pt > 0:
                ring_timer(ctx, 900, 560, 160, 1 - prog(lt, l1 + 2.0, L[1][1] + 1), '', pt)
                rich(ctx, [('15–60', C['yellow'])], 900, 545, 84, pt, pop=False)
                rich(ctx, [('minutes warning', C['white'])], 900, 790, 46, pt)
        title(ctx, [('We are not blind anymore', C['cyan'])], 120, 64, prog(lt, l0 + 0.3, l0 + 0.6))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    if l2 - 0.3 < lt < l3 + 0.3:
        a = prog(lt, l2 - 0.2, l2 + 0.3) * (1 - prog(lt, l3 - 0.2, l3 + 0.3))
        ctx.push_group()
        acts = [('reduce the load', C['yellow'], 0.2), ('Québec rebuilt its grid', C['cyan'], 1.6),
                ('satellites: safe mode', C['green'], 3.4), ('flights change course', C['pink'], 4.6)]
        for k, (lab, col, st) in enumerate(acts):
            p = eback(prog(lt, l2 + st, l2 + st + 0.4))
            if p <= 0: continue
            x = 270 + k * 460; y = 480
            ctx.save(); ctx.translate(x, y); ctx.scale(p, p); ctx.translate(-x, -y)
            circle(ctx, x, y, 150, '#20307e'); glow(ctx, x, y, 200, col, 0.35)
            if k == 0:
                ctx.new_path(); ctx.arc(x, y + 20, 80, math.pi, 2 * math.pi); ctx.set_line_width(18); src(ctx, C['white']); ctx.stroke()
                ang = math.pi + math.pi * lerp(0.85, 0.35, prog(lt, l2 + 0.6, l2 + 1.4))
                ctx.move_to(x, y + 20); ctx.line_to(x + 70 * math.cos(ang), y + 20 + 70 * math.sin(ang)); ctx.set_line_width(10)
                src(ctx, col); ctx.stroke()
            elif k == 1:
                pylon(ctx, x, y + 110, 0.8, C['white'])
                ctx.move_to(x + 40, y - 40); ctx.line_to(x + 70, y - 10); ctx.line_to(x + 120, y - 80); ctx.set_line_width(14); src(ctx, col)
                ctx.stroke()
            elif k == 2:
                satellite(ctx, x, y, 1.1, 0.2, panel=col)
            else:
                plane(ctx, x, y, 1.3, -0.3)
            ctx.restore()
            rich(ctx, [(lab, C['white'])], x, 720, 38, p, pop=False, maxw=430)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    if lt > l3 - 0.3:
        a = prog(lt, l3 - 0.2, l3 + 0.3)
        ctx.push_group()
        rich(ctx, [('catastrophe', C['red'])], 960, 420, 110, prog(lt, l3 + 0.3, l3 + 0.6))
        sk = prog(lt, l3 + 1.4, l3 + 1.9)
        if sk > 0:
            font(ctx, 110); w_ = ctx.text_extents('catastrophe').x_advance
            ctx.move_to(960 - w_ / 2 - 20, 420); ctx.line_to(960 - w_ / 2 - 20 + (w_ + 40) * sk, 420); ctx.set_line_width(14)
            src(ctx, C['white']); ctx.stroke()
        rich(ctx, [('a very bad week', C['yellow'])], 960, 620, 96, prog(lt, l3 + 2.2, l3 + 2.6))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


# ===================================================================== 7  OUTRO
def s7(ctx, lt, t, L):
    l0, l1, l2 = starts(L)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#03051a')); g.add_color_stop_rgba(1, *hexc('#14205a'))
    ctx.set_source(g); ctx.paint()
    for (x, y, r, ph, sp) in STARS: circle(ctx, x, y * 0.7, r, C['white'], 0.3 + 0.4 * (0.5 + 0.5 * math.sin(t * sp + ph)))
    au = prog(lt, 0.2, 2.0)
    aurora(ctx, 0, W, 60, 560, t, au)
    aurora(ctx, 200, 1700, 120, 500, t + 3, au * 0.6, cols=('#3ee0ff', '#b28cff', '#ff4f81'))
    # mountains + lake reflection
    ctx.new_path(); ctx.move_to(0, 700)
    for x, y in ((180, 520), (360, 640), (560, 460), (800, 650), (1020, 500), (1260, 660), (1480, 480), (1700, 620), (1920, 540)):
        ctx.line_to(x, y)
    ctx.line_to(W, 700); ctx.close_path(); src(ctx, '#0d1238'); ctx.fill()
    ctx.rectangle(0, 700, W, 380); src(ctx, '#0a1030'); ctx.fill()
    ctx.save(); ctx.rectangle(0, 700, W, 380); ctx.clip(); ctx.translate(0, 1400); ctx.scale(1, -1)
    aurora(ctx, 0, W, 60, 560, t, au * 0.35); ctx.restore()
    for k in range(8):
        y = 720 + k * 40; ctx.move_to(0, y); ctx.line_to(W, y); ctx.set_line_width(2); ctx.set_source_rgba(1, 1, 1, 0.04); ctx.stroke()
    pill(ctx, 300, 120, 'October 2026 · G3 storm', C['green'], C['dark'], 32, prog(lt, l0 + 0.4, l0 + 0.8))
    # solar cycle mini chart
    pc = prog(lt, l0 + 3.2, l0 + 4.4)
    if pc > 0:
        x0, y0 = 1380, 250
        ctx.new_path()
        for i in range(101):
            u = i / 100
            if u > pc: break
            x = x0 + u * 420; y = y0 - 110 * math.sin(math.pi * u) ** 2
            (ctx.move_to if i == 0 else ctx.line_to)(x, y)
        ctx.set_line_width(6); src(ctx, C['yellow']); ctx.stroke()
        if pc >= 1:
            mx = x0 + 0.62 * 420; my = y0 - 110 * math.sin(math.pi * 0.62) ** 2
            circle(ctx, mx, my, 12, C['pink']); pill(ctx, mx + 30, my - 50, 'we are here', C['pink'], C['white'], 24, 1)
        rich(ctx, [('11-year solar cycle', C['grey'])], x0 + 210, y0 + 40, 28, 1, w='normal', pop=False)
    pin = prog(lt, l1 - 0.2, l1 + 0.8)
    if pin > 0:
        person(ctx, 620, 720, 1.3, mono='#060a24', arm_l=0.3, arm_r=2.2)
        person(ctx, 700, 720, 1.1, mono='#060a24', arm_l=0.3, arm_r=0.4)
    if lt > l2 - 0.2:
        sp = eo(prog(lt, l2 + 1.4, l2 + 2.8))
        ctx.set_source_rgba(0.02, 0.02, 0.08, 0.5 * sp); ctx.paint()
        if sp > 0: sun(ctx, 960, lerp(1500, 520, sp), 220, t, loops=0.7, glow_a=sp)
        te = L[2][1]
        title(ctx, [("WHO'S REALLY ", C['white']), ('IN CHARGE', C['yellow'])], 900, 100, prog(lt, te + 0.2, te + 0.6))
