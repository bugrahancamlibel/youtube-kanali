from props_ice import *


def starts(L): return [a for a, b in L]


def fade_block(ctx, a, fn):
    if a <= 0: return
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def win(lt, a0, a1, f=0.25):
    return prog(lt, a0 - f, a0 + f) * (1 - prog(lt, a1 - f, a1 + f))


def label(ctx, txt, x, y, size, col, p, w='bold', maxw=900):
    rich(ctx, [(txt, col)], x, y, size, p, maxw=maxw, w=w)


def polar_bg(ctx, t, glow_col='#3a6ab8'):
    bg(ctx, t, top='#06143a', bot='#12306a', glow_col=glow_col, gy=560)


# ------------------------------------------------------------------ top view of the glacier + shelf
RIFTS = [[(860, 330), (800, 380), (760, 360), (700, 420), (650, 400), (600, 450)],
         [(880, 700), (820, 650), (780, 680), (720, 620), (660, 640), (600, 600)],
         [(760, 520), (720, 540), (680, 500), (630, 530), (590, 510)]]
SHARDS_TOP = [((420, 300), (640, 300), (600, 460), (430, 470)), ((430, 470), (600, 460), (620, 620), (440, 640)),
              ((440, 640), (620, 620), (650, 820), (430, 820)), ((640, 300), (900, 300), (880, 450), (600, 460)),
              ((600, 460), (880, 450), (900, 640), (620, 620)), ((620, 620), (900, 640), (900, 820), (650, 820))]


def topview(ctx, t, cracks=0.0, drift=0.0, flow=1.0, pin=1.0, grip=0.0, speed=1.0):
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgba(0, *hexc('#0a2556')); g.add_color_stop_rgba(1, *hexc('#163f86'))
    ctx.set_source(g); ctx.paint()
    for k in range(14):
        rnd = random.Random(k)
        x = (rnd.uniform(0, 900) - t * 12) % 900; y = rnd.uniform(60, 1020)
        ctx.move_to(x, y); ctx.line_to(x + 40, y); ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke()
    # pinning ridge (under the shelf)
    ctx.save(); ctx.translate(520, 560); ctx.scale(1.4, 1.0)
    circle(ctx, 0, 0, 70, '#0d1a40', pin); ctx.restore()
    # grounded glacier
    ctx.new_path(); ctx.move_to(W + 10, 120); ctx.curve_to(1500, 160, 1100, 230, 900, 290)
    ctx.line_to(900, 830); ctx.curve_to(1100, 880, 1500, 930, W + 10, 960); ctx.close_path()
    g = cairo.LinearGradient(900, 0, W, 0)
    g.add_color_stop_rgba(0, *hexc(ICE)); g.add_color_stop_rgba(1, *hexc('#ffffff'))
    ctx.set_source(g); ctx.fill()
    for k in range(6):
        y0 = 330 + k * 90
        ctx.move_to(W, y0 - 140 + k * 30); ctx.curve_to(1500, y0 - 70, 1200, y0 - 10, 900, y0)
        ctx.set_line_width(3); src(ctx, ICE3, 0.5); ctx.stroke()
    # shelf (floating)
    def shelf_piece(poly):
        ctx.new_path(); ctx.move_to(*poly[0])
        for p in poly[1:]: ctx.line_to(*p)
        ctx.close_path()
    if drift <= 0:
        ctx.new_path(); ctx.move_to(900, 300); ctx.curve_to(700, 290, 520, 270, 420, 300)
        ctx.curve_to(380, 460, 380, 680, 430, 820); ctx.curve_to(600, 840, 760, 830, 900, 820); ctx.close_path()
        src(ctx, ICE2, 0.92); ctx.fill_preserve(); ctx.set_line_width(5); src(ctx, '#ffffff', 0.7); ctx.stroke()
        circle(ctx, 520, 560, 70 * 1.0, '#0d1a40', 0.25 * pin)
    else:
        for k, poly in enumerate(SHARDS_TOP):
            rnd = random.Random(k * 31)
            dx = -drift * rnd.uniform(160, 420); dy = drift * rnd.uniform(-160, 160); rot = drift * rnd.uniform(-0.5, 0.5)
            cx = sum(p[0] for p in poly) / 4; cy = sum(p[1] for p in poly) / 4
            ctx.save(); ctx.translate(cx + dx, cy + dy); ctx.rotate(rot); ctx.scale(0.92, 0.92); ctx.translate(-cx, -cy)
            shelf_piece(poly); src(ctx, ICE2, 0.92); ctx.fill_preserve(); ctx.set_line_width(4); src(ctx, '#ffffff', 0.7); ctx.stroke()
            ctx.restore()
    if cracks > 0 and drift <= 0:
        for k, r in enumerate(RIFTS):
            c = clamp(cracks * 1.3 - k * 0.15)
            n = c * (len(r) - 1)
            if n <= 0: continue
            ctx.new_path(); ctx.move_to(*r[0])
            for i in range(1, int(n) + 1): ctx.line_to(*r[i])
            fr = n - int(n)
            if int(n) + 1 < len(r) and fr > 0:
                a_, b_ = r[int(n)], r[int(n) + 1]; ctx.line_to(lerp(a_[0], b_[0], fr), lerp(a_[1], b_[1], fr))
            ctx.set_line_width(9); ctx.set_line_join(cairo.LINE_JOIN_ROUND); src(ctx, '#0a2556', 0.9); ctx.stroke()
    if grip > 0:
        ctx.save(); ctx.translate(520, 560); ctx.scale(1.4, 1.0)
        ctx.new_path(); ctx.arc(0, 0, 90 + 8 * math.sin(t * 6), 0, 2 * math.pi); ctx.restore()
        ctx.set_line_width(8); ctx.set_dash([16, 10]); src(ctx, C['red'], grip); ctx.stroke(); ctx.set_dash([])
    if flow > 0:
        for k in range(6):
            ph = (t * 0.18 * speed + k / 6) % 1
            x = lerp(1820, 960, ph); y = 560 + (k % 3 - 1) * 150 * (0.6 + 0.4 * (1 - ph))
            al = flow * clamp(ph * 5) * clamp((1 - ph) * 5)
            ln = 60 * speed
            ctx.move_to(x + ln, y); ctx.line_to(x - 20, y); ctx.move_to(x - 20, y); ctx.line_to(x + 4, y - 16); ctx.move_to(x - 20, y); ctx.line_to(x + 4, y + 16)
            ctx.set_line_width(9); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['cyan'], al); ctx.stroke()


# ===================================================================== 0  COLD OPEN
def s0(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def mapview():
        polar_bg(ctx, t)
        z = eo(prog(lt, 0.0, 2.6))
        R = lerp(150, 420, z)
        antarctica(ctx, 960, 540, R, hi=prog(lt, l0 + 2.0, l0 + 2.6), t=t)
        penguin(ctx, 1560, 960, 1.1 * prog(lt, 0.8, 1.2), t)
        pf = prog(lt, l0 + 3.4, l0 + 4.0)
        if pf > 0:
            tx, ty = thwaites_xy(960, 540, R)
            florida(ctx, tx - 20, ty + 10, 150 * eback(pf), a=pf)
            pill(ctx, tx - 20, ty + 190, 'about the size of Florida', C['green'], C['dark'], 34, prog(lt, l0 + 3.8, l0 + 4.2))
        pill(ctx, 960, 90, 'Thwaites Glacier · West Antarctica', C['white'], C['dark'], 36, prog(lt, l0 + 2.2, l0 + 2.6))
    fade_block(ctx, 1 - prog(lt, l0 + 5.0, l0 + 5.5), mapview)

    def sideview():
        top, bottom = section(ctx, t, gl=900, shelf_front=380, flow=prog(lt, l0 + 7.2, l0 + 7.8))
        pr = prog(lt, l0 + 5.6, l0 + 6.2)
        if pr > 0:
            x = 1500; y0 = top(x); y1 = bottom(x)
            ctx.move_to(x, y0); ctx.line_to(x, y0 + (y1 - y0) * eo(pr)); ctx.set_line_width(8); src(ctx, C['yellow']); ctx.stroke()
            for yy in (y0, y1): ctx.move_to(x - 24, yy); ctx.line_to(x + 24, yy)
            ctx.set_line_width(8); src(ctx, C['yellow'], pr); ctx.stroke()
            pill(ctx, 1500, (y0 + y1) / 2, 'more than 2 km thick', C['yellow'], C['dark'], 38, pr)
        pill(ctx, 520, 160, 'sliding into the sea', C['cyan'], C['dark'], 40, prog(lt, l0 + 7.6, l0 + 8.0))
    fade_block(ctx, win(lt, l0 + 5.25, l1), sideview)

    def name():
        polar_bg(ctx, t, glow_col='#6a2a4a')
        antarctica(ctx, 1500, 620, 260, hi=1.0, t=t)
        rich(ctx, [('THWAITES', C['white'])], 700, 380, 150, prog(lt, l1 + 0.2, l1 + 0.6))
        rich(ctx, [('scientists call it', C['grey'])], 700, 250, 40, prog(lt, l1, l1 + 0.4), w='normal')
        stamp(ctx, 700, 620, 'THE DOOMSDAY GLACIER', C['red'], prog(lt, l1 + 2.0, l1 + 2.4), size=70)
    fade_block(ctx, win(lt, l1 - 0.2, l2), name)

    def shelf():
        topview(ctx, t, cracks=prog(lt, l2 + 1.4, l2 + 5.5), grip=prog(lt, l2 + 4.0, l2 + 4.6))
        pill(ctx, 640, 200, 'ICE SHELF', C['white'], C['dark'], 40, prog(lt, l2 + 0.4, l2 + 0.8))
        pill(ctx, 1380, 200, 'GLACIER', C['white'], C['dark'], 40, prog(lt, l2 + 0.6, l2 + 1.0))
        rich(ctx, [('poised to break apart', C['red'])], 960, 960, 54, prog(lt, l2 + 4.0, l2 + 4.4))
    fade_block(ctx, win(lt, l2 - 0.2, l3), shelf)

    te = L[3][1]
    def calve():
        top, bottom = section(ctx, t, gl=900, shelf_front=560, flow=1.0)
        k = prog(lt, l3 + 0.4, l3 + 2.6)
        iceberg(ctx, lerp(470, 330, k), SEA_Y - 10 + 60 * ss(k) ** 2, 1.25, rot=-0.9 * ss(k), seed=3)
        if k > 0.5:
            for j in range(10):
                ph = clamp((k - 0.5) * 2)
                circle(ctx, 400 + (j - 5) * 26 * ph * 3, SEA_Y - 70 * math.sin(math.pi * ph) * (1 + (j % 3) * 0.4), 9 * (1 - ph), '#e0f4ff', 1 - ph)
    fade_block(ctx, win(lt, l3 - 0.2, te + 0.3), calve)

    def ttl():
        polar_bg(ctx, t, glow_col='#7a2a4a')
        hills(ctx, 900, '#e8f4ff', amp=30, phase=0.3)
        hills(ctx, 960, '#bfe3f7', amp=18, phase=1.7)
        penguin(ctx, 260, 930, 1.3, t); penguin(ctx, 380, 950, 1.0, t, flip=-1); penguin(ctx, 1650, 940, 1.2, t, flip=-1)
        rich(ctx, [('WHAT IF', C['white'])], 960, 260, 90, prog(lt, te + 0.2, te + 0.5))
        rich(ctx, [('THE DOOMSDAY GLACIER', C['cyan'])], 960, 410, 120, prog(lt, te + 0.35, te + 0.65), maxw=1500)
        rich(ctx, [('COLLAPSED?', C['red'])], 960, 570, 130, prog(lt, te + 0.5, te + 0.8))
    fade_block(ctx, prog(lt, te + 0.1, te + 0.5), ttl)


# ===================================================================== 1  WHY DOOMSDAY
PX_M = 240
GROUND = 900


def ruler_scene(ctx, t, level_m, marks, lab=None, lab_p=0.0):
    polar_bg(ctx, t, glow_col='#2a5aa8')
    city(ctx, GROUND, t, 0.6, seed=12, x0=1100, x1=W)
    ctx.rectangle(0, GROUND, W, H - GROUND); src(ctx, '#2a3a6a'); ctx.fill()
    person(ctx, 760, GROUND, 1.9, shirt=C['orange'])
    rx = 520
    ctx.move_to(rx, GROUND); ctx.line_to(rx, GROUND - 3.1 * PX_M); ctx.set_line_width(16); src(ctx, '#f4f6ff'); ctx.stroke()
    for m in range(4):
        y = GROUND - m * PX_M
        ctx.move_to(rx - 30, y); ctx.line_to(rx + 30, y); ctx.set_line_width(6); src(ctx, '#f4f6ff'); ctx.stroke()
        rich(ctx, [(f'{m} m', C['white'])], rx - 90, y, 34, 1.0, pop=False)
    for cm in range(10, 300, 10):
        y = GROUND - cm / 100 * PX_M
        ctx.move_to(rx - 12, y); ctx.line_to(rx + 12, y); ctx.set_line_width(3); src(ctx, '#f4f6ff', 0.6); ctx.stroke()
    if level_m > 0:
        water_fill(ctx, GROUND - level_m * PX_M, t)
    for (m, txt, col, p) in marks:
        if p <= 0: continue
        y = GROUND - m * PX_M
        ctx.move_to(rx + 30, y); ctx.line_to(rx + 1300, y); ctx.set_dash([14, 10]); ctx.set_line_width(5); src(ctx, col, p); ctx.stroke(); ctx.set_dash([])
        pill(ctx, 1150, y - 46, txt, col, C['dark'], 40, p)


def s1(ctx, lt, t, L):
    l0, l1 = starts(L)

    def r1():
        lv = 0.65 * ss(prog(lt, l0 + 1.4, l0 + 4.0))
        ruler_scene(ctx, t, lv, [(0.65, '+65 cm  (Thwaites alone)', C['cyan'], prog(lt, l0 + 3.6, l0 + 4.0))])
        label(ctx, 'IF ALL OF THWAITES MELTED', 960, 100, 60, C['white'], prog(lt, l0 + 0.2, l0 + 0.6))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), r1)

    def cork():
        polar_bg(ctx, t, glow_col='#3a4aa8')
        co = prog(lt, l1 + 6.8, l1 + 7.6)
        bottle(ctx, 960, 600, 1.35, cork_out=co, t=t)
        rich(ctx, [('WEST ANTARCTIC ICE SHEET', ICE)], 960, 110, 56, prog(lt, l1 + 3.0, l1 + 3.4))
        pc = prog(lt, l1 + 3.4, l1 + 3.8) * (1 - co)
        pill(ctx, 1260, 260, 'Thwaites = the cork', C['yellow'], C['dark'], 40, pc)
    fade_block(ctx, win(lt, l1 - 0.2, l1 + 8.4), cork)

    def r3():
        lv = lerp(0.65, 3.05, ss(prog(lt, l1 + 8.6, l1 + 11.2)))
        ruler_scene(ctx, t, lv, [(0.65, '+65 cm', C['cyan'], 1.0), (3.0, '+3 m or more  (West Antarctica)', C['red'], prog(lt, l1 + 10.4, l1 + 10.8))])
    fade_block(ctx, prog(lt, l1 + 8.2, l1 + 8.6), r3)


# ===================================================================== 2  MELTING FROM BELOW
def s2(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def split():
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#ffb36a')); g.add_color_stop_rgba(1, *hexc('#ff7a5a'))
        ctx.set_source(g); ctx.paint()
        circle(ctx, 480, 420, 120, '#fff3b0'); glow(ctx, 480, 420, 320, C['yellow'], 0.5)
        rich(ctx, [('WARM AIR', C['white'])], 480, 760, 70, prog(lt, l0 + 0.2, l0 + 0.5))
        x_mark(ctx, 480, 420, 140, prog(lt, l0 + 1.0, l0 + 1.4))
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#123a7a')); g.add_color_stop_rgba(1, *hexc('#0a2556'))
        ctx.set_source(g); ctx.paint()
        for k in range(5):
            ph = (t * 0.3 + k / 5) % 1
            y = 300 + k * 100
            ctx.new_path()
            for x in range(1000, 1900, 12): ctx.line_to(x, y + 20 * math.sin(x / 60 + t * 3 + k))
            ctx.set_line_width(10); src(ctx, WARM, 0.6 + 0.3 * math.sin(t + k)); ctx.stroke()
        rich(ctx, [('WARM WATER', WARM)], 1440, 760, 70, prog(lt, l0 + 1.6, l0 + 1.9))
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), split)

    def below():
        tide = (0.6 + 0.4 * math.sin(t * 2.5)) * prog(lt, l1 + 6.0, l1 + 6.8)
        section(ctx, t, gl=900, shelf_front=380, warm=prog(lt, l1 + 0.2, l1 + 1.0), melt=prog(lt, l1 + 3.0, l1 + 3.6), tide=tide)
        pill(ctx, 260, 960, 'warm deep water', WARM, C['dark'], 36, prog(lt, l1 + 0.8, l1 + 1.2))
        pt = prog(lt, l1 + 7.0, l1 + 7.4)
        if pt > 0:
            y = bed_y(1000) + 50
            ctx.move_to(900, y); ctx.line_to(1070, y); ctx.set_line_width(6); src(ctx, C['yellow'], pt); ctx.stroke()
            for x in (900, 1070): ctx.move_to(x, y - 16); ctx.line_to(x, y + 16)
            ctx.stroke()
            pill(ctx, 985, y + 60, 'up to 10 km', C['yellow'], C['dark'], 36, pt)
        label(ctx, 'melting from below', 960, 120, 60, C['white'], prog(lt, l1 + 0.4, l1 + 0.8))
    fade_block(ctx, win(lt, l1 - 0.2, l2), below)

    def deeper():
        r = ss(prog(lt, l2 + 4.0, l2 + 7.6))
        gl = lerp(900, 1240, r)
        section(ctx, t, gl=gl, shelf_front=380 + 200 * r, warm=1.0, bed_hi=prog(lt, l2 + 0.6, l2 + 1.2), contact_hi=prog(lt, l2 + 5.0, l2 + 5.6) * (0.6 + 0.4 * math.sin(t * 5)))
        pa = prog(lt, l2 + 1.0, l2 + 1.5)
        if pa > 0:
            ctx.move_to(1300, 990); ctx.line_to(1780, 990); ctx.move_to(1780, 990); ctx.line_to(1750, 970); ctx.move_to(1780, 990); ctx.line_to(1750, 1010)
            ctx.set_line_width(7); src(ctx, C['yellow'], pa); ctx.stroke()
            rich(ctx, [('the bed gets deeper inland', C['yellow'])], 1540, 1040, 34, pa, pop=False)
        pill(ctx, gl, 240, 'grounding line retreats', C['white'], C['dark'], 36, prog(lt, l2 + 4.2, l2 + 4.6))
        label(ctx, 'more ice meets the water', 700, 110, 54, WARM, prog(lt, l2 + 5.4, l2 + 5.8))
    fade_block(ctx, win(lt, l2 - 0.2, l3), deeper)

    def lost():
        polar_bg(ctx, t, glow_col='#2a6ab8')
        hills(ctx, 900, '#1a2766', amp=0)
        n = int(60 * prog(lt, l3 + 0.4, l3 + 4.0))
        for k in range(n):
            row = 0; i = k; cap = 14
            while i >= cap: i -= cap; cap -= 1; row += 1
            x = 960 - (cap - 1) * 42 + i * 84; y = 860 - row * 70
            dropk = clamp((lt - (l3 + 0.4 + k * 0.06)) / 0.3)
            rrect(ctx, x - 36, y - 36 - 300 * (1 - eo(dropk)), 72, 64, 12); src(ctx, ICE if k % 2 else ICE2); ctx.fill()
        c = prog(lt, l3 + 0.4, l3 + 3.4)
        rich(ctx, [(counter_text(600e9 * eo(c)), C['white'])], 960, 170, 96, prog(lt, l3 + 0.2, l3 + 0.5))
        rich(ctx, [('tons of ice lost since the 1980s', C['cyan'])], 960, 270, 46, prog(lt, l3 + 1.0, l3 + 1.4), w='normal')
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), lost)


# ===================================================================== 3  THE BRAKE
def s3(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def brake():
        topview(ctx, t, flow=1.0)
        pill(ctx, 640, 200, 'FLOATING ICE SHELF', C['white'], C['dark'], 40, prog(lt, l0 + 1.4, l0 + 1.8))
        pr = prog(lt, l0 + 3.0, l0 + 3.4)
        if pr > 0:
            ctx.move_to(520, 640); ctx.line_to(420, 900); ctx.set_line_width(5); src(ctx, C['white'], pr); ctx.stroke()
            pill(ctx, 420, 940, 'pinned on an underwater ridge', C['yellow'], C['dark'], 34, pr)
        label(ctx, 'THE BRAKE', 1380, 960, 70, C['cyan'], prog(lt, l0 + 4.8, l0 + 5.2))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), brake)

    def failing():
        topview(ctx, t, cracks=prog(lt, l1 + 1.4, l1 + 5.6), grip=prog(lt, l1 + 6.2, l1 + 6.8))
        pill(ctx, 640, 180, 'cracks: up to 2 km a year', C['red'], C['white'], 40, prog(lt, l1 + 3.0, l1 + 3.4))
        pill(ctx, 520, 940, 'losing its grip', C['red'], C['white'], 36, prog(lt, l1 + 6.6, l1 + 7.0))
        label(ctx, 'THE BRAKE IS FAILING', 1380, 960, 60, C['red'], prog(lt, l1 + 0.2, l1 + 0.6))
    fade_block(ctx, win(lt, l1 - 0.2, l2), failing)

    def news():
        polar_bg(ctx, t, glow_col='#6a2a4a')
        pc = eback(prog(lt, l2 + 0.3, l2 + 0.8))
        def paper():
            card(ctx, 360, 220, 1200, 560, '#f4f1e8', 20, stroke=False)
            rrect(ctx, 360, 220, 1200, 90, 20); src(ctx, '#1f4a8a'); ctx.fill()
            rich(ctx, [('ANTARCTIC SCIENCE · 2026', C['white'])], 960, 266, 40, pop=False, shadow=False)
            rich(ctx, [('Doomsday Glacier ice shelf', C['dark'])], 960, 400, 70, pop=False, shadow=False)
            rich(ctx, [('"very likely" to break up', '#c0392b')], 960, 510, 84, pop=False, shadow=False)
            rich(ctx, [('this year', C['dark'])], 960, 610, 70, pop=False, shadow=False)
            rich(ctx, [('Robert Larter, British Antarctic Survey (May 2026)', '#6b7fb8')], 960, 710, 32, pop=False, shadow=False, w='normal')
        pop_scale(ctx, 960, 500, pc, paper)
    fade_block(ctx, win(lt, l2 - 0.2, l3), news)

    def breakup():
        d = ss(prog(lt, l3 + 0.6, l3 + 4.0))
        sp = 1 + 1.6 * prog(lt, l3 + 4.0, l3 + 5.0)
        topview(ctx, t, drift=max(0.001, d), speed=sp, pin=1.0)
        pill(ctx, 520, 940, 'no instant collapse', C['white'], C['dark'], 36, prog(lt, l3 + 1.0, l3 + 1.4))
        label(ctx, 'ICE FLOWS FASTER', 1380, 960, 64, C['cyan'], prog(lt, l3 + 4.4, l3 + 4.8))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), breakup)


# ===================================================================== 4  WHAT IF
def s4(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def imagine():
        polar_bg(ctx, t, glow_col='#7a2a4a')
        antarctica(ctx, 960, 560, 400, hi=1.0, t=t)
        tx, ty = thwaites_xy(960, 560, 400)
        k = prog(lt, l0 + 0.6, l0 + 1.8)
        circle(ctx, tx, ty, 120 * eo(k), OCEAN, k)
        label(ctx, 'IMAGINE', 960, 100, 80, C['white'], prog(lt, l0, l0 + 0.4))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), imagine)

    def centuries():
        polar_bg(ctx, t)
        y = 620
        ctx.move_to(200, y); ctx.line_to(1720, y); ctx.set_line_width(8); src(ctx, C['white'], 0.6); ctx.stroke()
        for k, yr in enumerate(('2026', '2100', '2200', '2300', '2400')):
            x = 260 + k * 350
            p = prog(lt, l1 + 0.6 + k * 0.4, l1 + 1.0 + k * 0.4)
            circle(ctx, x, y, 14, C['white'], p)
            rich(ctx, [(yr, C['white'])], x, y + 60, 40, p, pop=False)
        pb = prog(lt, l1 + 2.6, l1 + 3.6)
        if pb > 0:
            g = cairo.LinearGradient(260, 0, 1660, 0)
            g.add_color_stop_rgba(0, *hexc(C['red'], 0.0)); g.add_color_stop_rgba(0.3, *hexc(C['red'], 0.5)); g.add_color_stop_rgba(1, *hexc(C['red'], 0.15))
            rrect(ctx, 260, y - 40, 1400 * eo(pb), 80, 40); ctx.set_source(g); ctx.fill()
            rich(ctx, [('full collapse: over centuries', C['red'])], 960, y - 110, 50, pb)
        hourglass(ctx, 960, 300, 0.9, t, a=prog(lt, l1 + 0.2, l1 + 0.6))
        rich(ctx, [('how fast? no one knows exactly', C['grey'])], 960, 820, 40, prog(lt, l1 + 4.8, l1 + 5.2), w='normal')
    fade_block(ctx, win(lt, l1 - 0.2, l2), centuries)

    def coast():
        polar_bg(ctx, t, glow_col='#2a5aa8')
        city(ctx, 760, t, 0.8, seed=8, x0=0, x1=900)
        ctx.rectangle(0, 760, 900, 320); src(ctx, '#3a4a7a'); ctx.fill()
        for k in range(5): house(ctx, 120 + k * 160, 760, 1.2, [C['orange'], C['pink'], C['cyan'], C['yellow'], C['green']][k])
        lv = lerp(860, 735, ss(prog(lt, l2 + 0.6, l2 + 3.2)))
        water_fill(ctx, lv, t, x0=0, x1=900)
        pill(ctx, 450, 160, '+65 cm', C['cyan'], C['dark'], 50, prog(lt, l2 + 1.6, l2 + 2.0))
        pc = prog(lt, l2 + 3.4, l2 + 3.8)
        if pc > 0:
            card(ctx, 1000, 220, 820, 640, '#16245e', 40)
            cnt = prog(lt, l2 + 3.6, l2 + 6.0)
            rich(ctx, [(f'{int(680 * eo(cnt))} million', C['yellow'])], 1410, 330, 90, pc)
            rich(ctx, [('people live in low-lying coastal areas', C['white'])], 1410, 420, 34, pc, w='normal', maxw=740)
            for i in range(40):
                r_, c_ = divmod(i, 10)
                pp = prog(lt, l2 + 3.8 + i * 0.04, l2 + 4.1 + i * 0.04)
                if pp > 0: mini(ctx, 1110 + c_ * 66, 560 + r_ * 80, 0, 1.6 * pp, [C['orange'], C['cyan'], C['pink'], C['green']][i % 4])
            source_line(ctx, 'IPCC Special Report on the Ocean and Cryosphere (2019)', pc)
    fade_block(ctx, win(lt, l2 - 0.2, l3), coast)

    def floods():
        polar_bg(ctx, t, glow_col='#2a4a9a')
        label(ctx, 'ONCE-A-CENTURY FLOODS', 960, 100, 64, C['white'], prog(lt, l3 + 1.0, l3 + 1.4))
        ev = prog(lt, l3 + 4.6, l3 + 8.0)
        for i in range(100):
            r_, c_ = divmod(i, 20)
            x = 290 + c_ * 70; y = 270 + r_ * 80
            p = prog(lt, l3 + 0.6 + i * 0.008, l3 + 0.9 + i * 0.008)
            on = i == 57 or (ev > 0 and i / 100 < ev)
            rrect(ctx, x - 28, y - 30, 56, 60, 10); src(ctx, C['cyan'] if on else '#26357a', p); ctx.fill()
            if on:
                ctx.new_path()
                for xx in range(int(x - 20), int(x + 21), 4): ctx.line_to(xx, y + 6 * math.sin(xx / 6 + t * 4))
                ctx.set_line_width(4); src(ctx, C['white'], p); ctx.stroke()
        rich(ctx, [('100 years', C['grey'])], 960, 700, 36, prog(lt, l3 + 1.4, l3 + 1.8), w='normal')
        pill(ctx, 960, 820, 'by 2050: every year, at many coasts', C['yellow'], C['dark'], 44, prog(lt, l3 + 6.0, l3 + 6.4))
        source_line(ctx, 'IPCC SROCC (2019)', prog(lt, l3 + 6.0, l3 + 6.4))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), floods)


# ===================================================================== 5  BELOW SEA LEVEL
def s5(ctx, lt, t, L):
    l0, l1 = starts(L)

    def dutch():
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#7ab0f0')); g.add_color_stop_rgba(1, *hexc('#d8ecff'))
        ctx.set_source(g); ctx.paint()
        circle(ctx, 1500, 200, 70, '#fff3c0'); glow(ctx, 1500, 200, 260, '#ffd23f', 0.4)
        sea = 520
        ctx.rectangle(0, sea, 700, H - sea); src(ctx, '#1d4fb0'); ctx.fill()
        for k in range(6):
            ctx.new_path()
            for x in range(0, 640, 12): ctx.line_to(x, sea + 40 + k * 70 + 8 * math.sin(x / 50 + t * 2 + k))
            ctx.set_line_width(4); ctx.set_source_rgba(1, 1, 1, 0.15); ctx.stroke()
        ctx.new_path()
        for x in range(0, 660, 10): ctx.line_to(x, sea + 8 * math.sin(x / 70 + t * 2.4))
        ctx.set_line_width(6); src(ctx, '#bfe3ff'); ctx.stroke()
        ctx.rectangle(700, 660, W - 700, H); src(ctx, '#4aa86a'); ctx.fill()
        ctx.rectangle(700, 700, W - 700, H); src(ctx, '#3a8a55'); ctx.fill()
        for k in range(4): house(ctx, 1000 + k * 170, 660, 1.3, [C['orange'], C['pink'], C['yellow'], C['cyan']][k])
        windmill(ctx, 1720, 660, 1.1, t)
        ctx.move_to(540, H); ctx.line_to(610, sea - 70); ctx.line_to(700, sea - 70); ctx.line_to(830, H); ctx.close_path(); src(ctx, '#5aa05a'); ctx.fill()
        ctx.move_to(610, sea - 70); ctx.line_to(700, sea - 70); ctx.set_line_width(10); src(ctx, '#6ac06a'); ctx.stroke()
        pill(ctx, 655, sea - 130, 'dike', C['white'], C['dark'], 32, prog(lt, l0 + 1.4, l0 + 1.8))
        pl = prog(lt, l0 + 2.4, l0 + 3.0)
        ctx.move_to(700, sea); ctx.line_to(700 + 1200 * eo(pl), sea); ctx.set_dash([16, 10]); ctx.set_line_width(5); src(ctx, '#1d4fb0', pl); ctx.stroke(); ctx.set_dash([])
        rich(ctx, [('sea level', '#1d4fb0')], 1000, sea - 30, 32, pl, pop=False)
        ctx.move_to(880, sea + 10); ctx.line_to(880, 655); ctx.set_line_width(6); src(ctx, C['red'], pl); ctx.stroke()
        rich(ctx, [('land below the sea', C['white'])], 1080, 740, 34, pl, pop=False)
        pill(ctx, 1240, 110, 'about 1/4 of the Netherlands lies below sea level', C['yellow'], C['dark'], 38, prog(lt, l0 + 3.0, l0 + 3.4))
        pill(ctx, 1240, 190, 'protected by dikes, dunes and storm barriers', C['white'], C['dark'], 32, prog(lt, l0 + 5.6, l0 + 6.0))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), dutch)

    def choice():
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        polar_bg(ctx, t, glow_col='#2a5aa8')
        city(ctx, 820, t, 0.8, seed=19, x0=380, x1=960)
        ctx.rectangle(340, 820, W / 2, 260); src(ctx, '#3a4a7a'); ctx.fill()
        wh = 120 + 300 * ss(prog(lt, l1 + 0.8, l1 + 2.4))
        water_fill(ctx, 820 - wh + 50, t, x0=0, x1=290)
        rrect(ctx, 280, 820 - wh, 70, wh + 260, 8); src(ctx, '#9aa6cf'); ctx.fill()
        rich(ctx, [('BUILD WALLS', C['cyan'])], 480, 140, 80, prog(lt, l1 + 0.4, l1 + 0.8))
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        bg(ctx, t, top='#2a1a4a', bot='#4a2a5a', glow_col='#8a4a6a', gx=1440, gy=560)
        hills(ctx, 860, '#3a2a5a', amp=0)
        mv = ss(prog(lt, l1 + 2.6, l1 + 5.4))
        for k in range(3):
            x = lerp(1060 + k * 150, 1420 + k * 150, mv)
            bob = abs(math.sin(t * 8 + k)) * 10 * (0 < mv < 1)
            person(ctx, x, 860 - bob, 1.4, shirt=[C['orange'], C['pink'], C['green']][k], arm_l=1.2, arm_r=1.2)
            box(ctx, x, 600 - bob, 0.9)
        rich(ctx, [('OR MOVE', C['pink'])], 1440, 140, 80, prog(lt, l1 + 2.6, l1 + 3.0))
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    fade_block(ctx, prog(lt, l1 - 0.2, l1 + 0.3), choice)


# ===================================================================== 6  THE CURTAIN
def s6(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def curtain():
        cu = ss(prog(lt, l1 + 0.6, l1 + 2.6))
        section(ctx, t, gl=900, shelf_front=380, warm=1.0, curtain=cu, curtain_x=230)
        label(ctx, 'A CURTAIN UNDER THE SEA', 960, 110, 74, C['white'], prog(lt, l0 + 0.6, l0 + 1.0))
        pa = prog(lt, l1 + 2.4, l1 + 2.8)
        if pa > 0:
            y = bed_y(230)
            ctx.move_to(130, y - 300); ctx.line_to(130, y); ctx.set_line_width(6); src(ctx, C['yellow'], pa); ctx.stroke()
            for yy in (y - 300, y): ctx.move_to(110, yy); ctx.line_to(150, yy)
            ctx.stroke()
            pill(ctx, 330, 300, '~600 m down', C['yellow'], C['dark'], 36, pa)
            pill(ctx, 960, 240, '80 km long', C['yellow'], C['dark'], 44, prog(lt, l1 + 1.0, l1 + 1.4))
        pb = prog(lt, l1 + 4.0, l1 + 4.4)
        rich(ctx, [('warm water: blocked', WARM)], 600, 980, 44, pb)
    fade_block(ctx, 1 - prog(lt, l2 - 0.2, l2 + 0.3), curtain)

    def price():
        polar_bg(ctx, t, glow_col='#6a5a1a')
        for k in range(14):
            rnd = random.Random(k * 5)
            ph = (t * 0.25 + k / 14) % 1
            money(ctx, rnd.uniform(200, 1720), lerp(-80, 1150, ph), 1.0, rot=t * rnd.uniform(-1, 1), a=0.6)
        pt = prog(lt, l2 + 0.6, l2 + 1.1)
        price_tag(ctx, 960, 470, 1.25 * eback(pt), '$40-80 BILLION', 'to build it', a=pt)
        pill(ctx, 960, 760, '+ up to $2 billion every year', C['white'], C['dark'], 44, prog(lt, l2 + 3.0, l2 + 3.4))
        label(ctx, 'THE PRICE', 960, 120, 70, C['yellow'], prog(lt, l2 + 0.2, l2 + 0.6))
    fade_block(ctx, win(lt, l2 - 0.2, l3), price)

    def critics():
        polar_bg(ctx, t, glow_col='#4a2a6a')
        for k, (txt, col) in enumerate((('too risky', C['red']), ('too remote', C['orange']), ('a distraction from cutting emissions', C['pink']))):
            st = l3 + 0.8 + k * 1.1
            pill(ctx, 960, 280 + k * 140, txt, col, C['white'], 50, prog(lt, st, st + 0.3))
        rich(ctx, [('CRITICS SAY', C['white'])], 960, 130, 70, prog(lt, l3 + 0.2, l3 + 0.6))
        pn = prog(lt, l3 + 5.6, l3 + 6.0)
        if pn > 0:
            card(ctx, 560, 720, 800, 200, '#16245e', 40)
            rich(ctx, [('first test: Norway, 2027', C['cyan'])], 960, 790, 52, pn)
            rich(ctx, [('(if funding allows)', C['grey'])], 960, 860, 32, pn, w='normal')
        source_line(ctx, 'Proposal: Moore, Wolovick et al.; critique: Siegert et al., Frontiers in Science (2025)', prog(lt, l3 + 1.0, l3 + 1.4))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), critics)


# ===================================================================== 7  THE WARNING
def s7(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def under():
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#0f3a7a')); g.add_color_stop_rgba(1, *hexc('#04102e'))
        ctx.set_source(g); ctx.paint()
        ctx.new_path(); ctx.move_to(0, 0)
        for x in range(0, W + 1, 40): ctx.line_to(x, 200 + 40 * math.sin(x / 130) + 20 * math.sin(x / 47))
        ctx.line_to(W, 0); ctx.close_path(); src(ctx, ICE2); ctx.fill()
        for k in range(20):
            rnd = random.Random(k)
            ph = (t * 0.1 * rnd.uniform(0.5, 1.5) + rnd.random()) % 1
            circle(ctx, rnd.uniform(0, W), lerp(1080, 240, ph), rnd.uniform(2, 5), '#bfe8ff', 0.4 * (1 - ph))
        x = lerp(2200, 700, ss(prog(lt, l0 + 0.4, l0 + 6.0)))
        icefin(ctx, x, 420 + 20 * math.sin(t * 1.5), 1.0, t)
        pill(ctx, 960, 900, 'Icefin robot · under Thwaites, 2020', C['yellow'], C['dark'], 40, prog(lt, l0 + 5.0, l0 + 5.4))
        for k in range(5):
            p = prog(lt, l0 + 6.2 + k * 0.3, l0 + 6.5 + k * 0.3)
            pill(ctx, 1150 + k * 130, 620 - k * 40, ['temp', 'salt', 'melt', 'flow', 'depth'][k], C['cyan'], C['dark'], 28, p)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), under)

    def nottom():
        polar_bg(ctx, t)
        antarctica(ctx, 560, 560, 330, hi=1.0, t=t)
        pc = prog(lt, l1 + 1.6, l1 + 2.0)
        calendar(ctx, 1400, 400, 1.1 * eback(pc), 'TOMORROW?', 'NO', col=C['green'], big_col=C['green'])
        rich(ctx, [('Not tomorrow.', C['white'])], 1400, 640, 50, pc)
        pr = prog(lt, l1 + 3.6, l1 + 4.0)
        if pr > 0:
            rrect(ctx, 960, 760, 880, 80, 12); src(ctx, '#f4f6ff', pr); ctx.fill()
            for k in range(31):
                x = 985 + k * 27.5
                lit = prog(lt, l1 + 3.8 + k * 0.05, l1 + 3.9 + k * 0.05)
                ctx.move_to(x, 760); ctx.line_to(x, 760 + (46 if k % 10 == 0 else 26)); ctx.set_line_width(4)
                src(ctx, C['red'] if lit > 0.5 else C['dark'], pr); ctx.stroke()
            rich(ctx, [('every centimeter counts', C['white'])], 1400, 890, 44, pr)
    fade_block(ctx, win(lt, l1 - 0.2, l2), nottom)

    def actions():
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        polar_bg(ctx, t, glow_col='#2a8a6a')
        hills(ctx, 860, '#1a4a3a', amp=20)
        thermometer(ctx, 260, 620, 1.3, lerp(0.85, 0.45, ss(prog(lt, l2 + 1.0, l2 + 3.0))), col=C['red'])
        for k in range(3): turbine(ctx, 480 + k * 150, 860, 0.9 + 0.1 * k, t + k)
        solar_panel(ctx, 760, 800, 0.9)
        rich(ctx, [('SLOW THE WARMING', C['green'])], 480, 140, 64, prog(lt, l2 + 0.6, l2 + 1.0))
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        polar_bg(ctx, t, glow_col='#2a5aa8')
        ctx.rectangle(W / 2, 760, W / 2, 320); src(ctx, '#3a4a7a'); ctx.fill()
        for k in range(4): house(ctx, 1260 + k * 160, 760, 1.2, [C['orange'], C['pink'], C['cyan'], C['yellow']][k])
        wp = ss(prog(lt, l2 + 3.0, l2 + 4.2))
        rrect(ctx, 1080, 760 - 240 * wp, 60, 240 * wp + 320, 8); src(ctx, '#9aa6cf'); ctx.fill()
        water_fill(ctx, 640, t, x0=W / 2, x1=1080)
        rich(ctx, [('GET COASTS READY', C['cyan'])], 1440, 140, 64, prog(lt, l2 + 2.6, l2 + 3.0))
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    fade_block(ctx, win(lt, l2 - 0.2, l3), actions)

    def final():
        polar_bg(ctx, t, glow_col='#6a4a1a')
        hills(ctx, 860, '#e8f4ff', amp=40, phase=0.4)
        hills(ctx, 940, '#bfe3f7', amp=20, phase=2.2)
        penguin(ctx, 1600, 900, 1.3, t, flip=-1); penguin(ctx, 1720, 920, 1.0, t)
        warning_sign(ctx, 960, 380, 1.3 * eback(prog(lt, l3 + 0.2, l3 + 0.7)), t=t)
        rich(ctx, [('NOT A COUNTDOWN.', C['white'])], 960, 660, 80, prog(lt, l3 + 0.6, l3 + 1.0))
        rich(ctx, [('A WARNING.', C['yellow'])], 960, 780, 100, prog(lt, l3 + 2.0, l3 + 2.4))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), final)
