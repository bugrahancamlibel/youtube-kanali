import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'qday'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'aijobs'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solar'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'long'))
from props_q import *
from render import mini

ICE = '#eaf6ff'
ICE2 = '#bfe3f7'
ICE3 = '#8cc8ea'
OCEAN = '#123a7a'
OCEAN2 = '#0a2556'
WARM = '#ff8a3d'
ROCK = '#5a3f3a'
ROCK2 = '#3f2b2a'


# ------------------------------------------------------------------ maps
def _ant_r(lon):
    """Very stylised radius of Antarctica for a longitude in degrees (0 = up)."""
    l = (lon + 180) % 360 - 180
    r = 1.0 + 0.05 * math.sin(math.radians(l * 5))
    def bump(c, w, amp):
        d = (l - c + 180) % 360 - 180
        return amp * math.exp(-(d / w) ** 2)
    r += bump(180, 22, -0.42)     # Ross Sea
    r += bump(-130, 40, -0.22)    # West Antarctica is smaller
    r += bump(-106, 6, -0.07)     # Amundsen Sea dent
    r += bump(-40, 16, -0.33)     # Weddell Sea
    r += bump(-62, 4.5, 0.52)     # Peninsula
    r += bump(-58, 2.5, 0.18)
    r += bump(70, 18, -0.12)      # Amery
    return r


ANT = [(0.0, -0.95), (0.3, -0.92), (0.55, -0.85), (0.75, -0.7), (0.85, -0.52), (0.78, -0.38), (0.95, -0.3), (1.0, 0.0),
       (0.98, 0.25), (0.9, 0.5), (0.75, 0.7), (0.55, 0.85), (0.35, 0.9), (0.25, 0.75), (0.15, 0.55), (0.0, 0.45),
       (-0.15, 0.5), (-0.25, 0.62), (-0.35, 0.75), (-0.55, 0.7), (-0.7, 0.55), (-0.74, 0.42), (-0.66, 0.34),
       (-0.8, 0.25), (-0.85, 0.1), (-0.78, -0.05), (-0.9, -0.2), (-1.05, -0.4), (-1.2, -0.62), (-1.32, -0.84),
       (-1.24, -0.86), (-1.1, -0.68), (-0.95, -0.52), (-0.78, -0.44), (-0.6, -0.46), (-0.45, -0.56), (-0.35, -0.72),
       (-0.2, -0.86)]


def _chaikin(pts, n=2):
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            out += [(0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]), (0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1])]
        pts = out
    return pts


ANT_S = _chaikin(ANT, 3)


def antarctica(ctx, cx, cy, R, a=1.0, hi=0.0, t=0.0, col=None):
    if R <= 2 or a <= 0: return
    pts = [(cx + R * x, cy + R * y) for x, y in ANT_S]
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path()
    path = ctx.copy_path()
    src(ctx, ICE3, a); ctx.save(); ctx.translate(0, R * 0.03); ctx.new_path(); ctx.append_path(path); ctx.fill(); ctx.restore()
    ctx.new_path(); ctx.append_path(path)
    g = cairo.RadialGradient(cx - R * 0.2, cy - R * 0.2, R * 0.1, cx, cy, R * 1.2)
    g.add_color_stop_rgba(0, *hexc('#ffffff', a)); g.add_color_stop_rgba(1, *hexc(col or ICE2, a))
    ctx.set_source(g); ctx.fill()
    if hi > 0:
        tx, ty = thwaites_xy(cx, cy, R)
        glow(ctx, tx, ty, R * 0.35, C['red'], 0.55 * hi * (0.75 + 0.25 * math.sin(t * 4)))
        circle(ctx, tx, ty, R * 0.07, C['red'], hi * a)
        ctx.new_path(); ctx.arc(tx, ty, R * 0.07 + R * 0.08 * ((t * 0.8) % 1), 0, 2 * math.pi)
        ctx.set_line_width(R * 0.012); src(ctx, C['red'], hi * a * (1 - (t * 0.8) % 1)); ctx.stroke()


def thwaites_xy(cx, cy, R):
    return cx - R * 0.6, cy + R * 0.36


FLORIDA = [(-1.0, -0.62), (-0.2, -0.66), (0.05, -0.62), (0.12, -0.70), (0.25, -0.62), (0.35, -0.35), (0.45, -0.05),
           (0.55, 0.30), (0.58, 0.60), (0.50, 0.85), (0.40, 0.92), (0.30, 0.80), (0.18, 0.55), (0.05, 0.30),
           (-0.02, 0.05), (-0.08, -0.25), (-0.20, -0.42), (-0.45, -0.45), (-0.70, -0.50), (-1.0, -0.52)]


def florida(ctx, cx, cy, s, a=1.0, col=None, outline=True):
    if s <= 1 or a <= 0: return
    ctx.new_path(); ctx.move_to(cx + FLORIDA[0][0] * s, cy + FLORIDA[0][1] * s)
    for x, y in FLORIDA[1:]: ctx.line_to(cx + x * s, cy + y * s)
    ctx.close_path()
    src(ctx, col or C['green'], 0.55 * a); ctx.fill_preserve()
    ctx.set_line_width(5); ctx.set_dash([12, 8]); src(ctx, C['white'], a if outline else 0); ctx.stroke(); ctx.set_dash([])


# ------------------------------------------------------------------ cross-section
SEA_Y = 400


def bed_y(x):
    if x < 260: return 880
    if x < 560: return 880 - 410 * math.sin(math.pi * (x - 260) / 300) ** 2
    if x < 700: return 880 - 100 * ss((x - 560) / 140)
    return 780 + (x - 700) * 0.08


def section(ctx, t, gl=900, shelf_front=380, warm=0.0, tide=0.0, bed_hi=0.0, contact_hi=0.0, flow=0.0, sky=True,
            melt=0.0, a=1.0, curtain=0.0, curtain_x=300):
    """Glacier cross-section: ocean left, inland right. gl = grounding-line x."""
    if sky:
        g = cairo.LinearGradient(0, 0, 0, SEA_Y)
        g.add_color_stop_rgba(0, *hexc('#1b2f7a')); g.add_color_stop_rgba(1, *hexc('#6a8ad8'))
        ctx.set_source(g); ctx.rectangle(0, 0, W, SEA_Y); ctx.fill()
    g = cairo.LinearGradient(0, SEA_Y, 0, H)
    g.add_color_stop_rgba(0, *hexc(OCEAN)); g.add_color_stop_rgba(1, *hexc(OCEAN2))
    ctx.set_source(g); ctx.rectangle(0, SEA_Y, W, H - SEA_Y); ctx.fill()
    # warm water (deep layer)
    if warm > 0:
        g = cairo.LinearGradient(0, 640, 0, 900)
        g.add_color_stop_rgba(0, *hexc(WARM, 0)); g.add_color_stop_rgba(1, *hexc(WARM, 0.35 * warm))
        ctx.set_source(g); ctx.rectangle(0, 640, W, 300); ctx.fill()
    # bed
    ctx.new_path(); ctx.move_to(0, H)
    for x in range(0, W + 1, 10): ctx.line_to(x, bed_y(x))
    ctx.line_to(W, H); ctx.close_path(); src(ctx, ROCK); ctx.fill()
    ctx.new_path()
    for x in range(0, W + 1, 10): ctx.line_to(x, bed_y(x) + 16)
    ctx.set_line_width(6); src(ctx, ROCK2); ctx.stroke()
    if bed_hi > 0:
        ctx.new_path()
        for x in range(int(gl), W + 1, 10): ctx.line_to(x, bed_y(x))
        ctx.set_line_width(10); src(ctx, C['yellow'], bed_hi); ctx.stroke()
    # ice
    def top(x):
        if x <= gl: return SEA_Y - 34 - 12 * (x - shelf_front) / max(1, gl - shelf_front)
        u = clamp((x - gl) / (W + 60 - gl))
        return SEA_Y - 46 - 300 * u ** 0.55
    def bottom(x):
        if x >= gl: return bed_y(x)
        u = clamp((x - shelf_front) / max(1, gl - shelf_front))
        return SEA_Y + 60 + (bed_y(gl) - SEA_Y - 60) * u ** 2.2
    xs = [shelf_front] + list(range(int(shelf_front) + 1, W + 61, 8))
    ctx.new_path(); ctx.move_to(shelf_front, top(shelf_front))
    for x in xs: ctx.line_to(x, top(x))
    for x in reversed(xs): ctx.line_to(x, bottom(x))
    ctx.close_path()
    g = cairo.LinearGradient(0, 80, 0, 900)
    g.add_color_stop_rgba(0, *hexc('#ffffff', a)); g.add_color_stop_rgba(0.5, *hexc(ICE, a)); g.add_color_stop_rgba(1, *hexc(ICE3, a))
    ctx.set_source(g); ctx.fill()
    # ice layering
    for k in range(1, 5):
        ctx.new_path()
        for x in xs:
            if x < shelf_front + 10: continue
            yt, yb = top(x), bottom(x)
            ctx.line_to(x, yt + (yb - yt) * k / 5)
        ctx.set_line_width(2); ctx.set_source_rgba(0.55, 0.75, 0.9, 0.35 * a); ctx.stroke()
    # flow arrows on the surface
    if flow > 0:
        for k in range(5):
            ph = (t * 0.25 * (1 + flow) + k / 5) % 1
            x = lerp(1800, shelf_front + 40, ph)
            y = top(x) - 30
            ctx.move_to(x + 40, y); ctx.line_to(x - 30, y); ctx.move_to(x - 30, y); ctx.line_to(x - 8, y - 14)
            ctx.move_to(x - 30, y); ctx.line_to(x - 8, y + 14)
            ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['cyan'], 0.9 * flow * (1 - abs(ph - 0.5) * 1.6)); ctx.stroke()
    # warm water arrows under the shelf
    if warm > 0:
        for k in range(7):
            ph = (t * 0.22 + k / 7) % 1
            x = lerp(60, gl - 20, ph)
            if curtain > 0.3 and x > curtain_x - 30:
                x = curtain_x - 30; y = 760 - 120 * ((ph * 7) % 1)
            else:
                y = 820 - 30 * math.sin(ph * 6 + k) if x < shelf_front + 60 else min(bottom(x) + 26, 820)
            al = warm * clamp(ph * 6) * clamp((1 - ph) * 6)
            ctx.move_to(x - 50, y); ctx.line_to(x + 20, y); ctx.move_to(x + 20, y); ctx.line_to(x, y - 14); ctx.move_to(x + 20, y); ctx.line_to(x, y + 14)
            ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, WARM, al); ctx.stroke()
    if melt > 0:
        for k in range(10):
            ph = (t * 0.6 + k / 10) % 1
            x = lerp(shelf_front + 60, gl - 30, (k * 0.37) % 1)
            circle(ctx, x, bottom(x) + 6 + 40 * ph, 5, '#bfe8ff', melt * (1 - ph))
    if tide > 0:
        ln = 170 * tide
        ctx.new_path(); ctx.move_to(gl - 10, bed_y(gl) - 2)
        for x in range(int(gl), int(gl + ln), 6): ctx.line_to(x, bed_y(x) - 9 * (1 - (x - gl) / ln))
        for x in range(int(gl + ln), int(gl) - 1, -6): ctx.line_to(x, bed_y(x))
        ctx.close_path(); src(ctx, WARM, 0.9); ctx.fill()
    if contact_hi > 0:
        ctx.new_path()
        for x in range(int(shelf_front), int(gl) + 1, 8): ctx.line_to(x, bottom(x))
        ctx.set_line_width(10); src(ctx, WARM, contact_hi); ctx.stroke()
    if curtain > 0:
        cx = curtain_x; ytop = bed_y(cx) - 300 * curtain
        for k in range(9):
            yy = ytop + k * (bed_y(cx) - ytop) / 9
            ctx.move_to(cx - 6 * math.sin(t * 2 + k), yy); ctx.line_to(cx + 6 * math.sin(t * 2 + k + 1), yy + (bed_y(cx) - ytop) / 9)
        ctx.set_line_width(22); src(ctx, '#ffd23f', 0.9); ctx.stroke()
        circle(ctx, cx, ytop - 14, 16, C['pink'])
        ctx.move_to(cx, ytop - 14); ctx.line_to(cx, ytop); ctx.set_line_width(4); src(ctx, C['white']); ctx.stroke()
    return top, bottom


# ------------------------------------------------------------------ other props
def ruler(ctx, x, y0, y1, a=1.0, ticks=((0, '0'),), unit_px=1.0):
    ctx.move_to(x, y0); ctx.line_to(x, y1); ctx.set_line_width(14); src(ctx, '#f4f6ff', a); ctx.stroke()


def water_fill(ctx, level_y, t, a=1.0, x0=0, x1=W):
    ctx.new_path(); ctx.move_to(x0, H)
    for x in range(int(x0), int(x1) + 11, 10):
        ctx.line_to(x, level_y + 8 * math.sin(x / 70 + t * 2.4))
    ctx.line_to(x1, H); ctx.close_path()
    src(ctx, '#2d6be0', 0.72 * a); ctx.fill()
    ctx.new_path()
    for x in range(int(x0), int(x1) + 11, 10):
        ctx.line_to(x, level_y + 8 * math.sin(x / 70 + t * 2.4))
    ctx.set_line_width(5); src(ctx, '#bfe3ff', 0.9 * a); ctx.stroke()


def bottle(ctx, x, y, s, cork_out=0.0, a=1.0, t=0.0):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-60, -150); ctx.line_to(-60, -210); ctx.line_to(60, -210); ctx.line_to(60, -150)
    ctx.curve_to(170, -120, 190, -60, 190, 20); ctx.line_to(190, 230); ctx.curve_to(190, 260, 170, 280, 140, 280)
    ctx.line_to(-140, 280); ctx.curve_to(-170, 280, -190, 260, -190, 230); ctx.line_to(-190, 20)
    ctx.curve_to(-190, -60, -170, -120, -60, -150); ctx.close_path()
    path = ctx.copy_path()
    ctx.set_source_rgba(0.75, 0.9, 1, 0.22 * a); ctx.fill()
    ctx.save(); ctx.new_path(); ctx.append_path(path); ctx.clip()
    lvl = lerp(-40, 120, ss(cork_out))
    ctx.rectangle(-200, lvl, 400, 400); src(ctx, ICE, 0.95 * a); ctx.fill()
    for k in range(6):
        rrect(ctx, -150 + k * 50, lvl + 30 + (k % 2) * 40, 40, 40, 8); src(ctx, ICE2, a); ctx.fill()
    ctx.restore()
    ctx.new_path(); ctx.append_path(path); ctx.set_line_width(8); ctx.set_source_rgba(1, 1, 1, 0.7 * a); ctx.stroke()
    cy = -235 - 260 * eo(cork_out); rot = 2.5 * cork_out
    ctx.save(); ctx.translate(120 * cork_out, cy); ctx.rotate(rot)
    rrect(ctx, -52, -40, 104, 80, 12); src(ctx, '#c08a5a', a); ctx.fill()
    for k in range(5): circle(ctx, -30 + k * 15, -10 + (k % 2) * 18, 4, '#8c5a2a', a)
    ctx.restore()
    if cork_out > 0.2:
        for k in range(8):
            ph = clamp((cork_out - 0.2) * 1.4)
            ang = -math.pi / 2 + (k - 3.5) * 0.25
            rrect(ctx, math.cos(ang) * 200 * ph - 15, -210 + math.sin(ang) * 200 * ph - 15, 30, 30, 6); src(ctx, ICE, a * (1 - ph))
            ctx.fill()
    ctx.restore()


def windmill(ctx, x, y, s, t, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-50, 0); ctx.line_to(-30, -200); ctx.line_to(30, -200); ctx.line_to(50, 0); ctx.close_path(); src(ctx, '#8c5a3a', a); ctx.fill()
    ctx.move_to(-38, -200); ctx.line_to(0, -250); ctx.line_to(38, -200); ctx.close_path(); src(ctx, '#5a3a2a', a); ctx.fill()
    rrect(ctx, -14, -40, 28, 40, 8); src(ctx, '#3a2a1a', a); ctx.fill()
    ctx.save(); ctx.translate(0, -200); ctx.rotate(t * 0.8)
    for k in range(4):
        ctx.save(); ctx.rotate(k * math.pi / 2)
        ctx.rectangle(-6, -170, 12, 170); src(ctx, '#d4dcf2', a); ctx.fill()
        ctx.rectangle(6, -160, 40, 120); src(ctx, '#f4f6ff', 0.85 * a); ctx.fill()
        ctx.restore()
    circle(ctx, 0, 0, 12, '#3a2a1a', a)
    ctx.restore(); ctx.restore()


def iceberg(ctx, x, y, s, a=1.0, rot=0.0, seed=1):
    if s <= 1e-3 or a <= 0: return
    rnd = random.Random(seed)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    top = [(-120, 0), (-100, -60), (-40, -90), (10, -70), (60, -110), (120, -40), (130, 0)]
    ctx.new_path(); ctx.move_to(*top[0])
    for p in top[1:]: ctx.line_to(p[0] + rnd.uniform(-8, 8), p[1] + rnd.uniform(-8, 8))
    ctx.close_path(); src(ctx, '#ffffff', a); ctx.fill()
    ctx.new_path(); ctx.move_to(-130, 0); ctx.line_to(140, 0); ctx.line_to(90, 170); ctx.line_to(-80, 200); ctx.close_path()
    src(ctx, ICE3, 0.55 * a); ctx.fill()
    ctx.restore()


def penguin(ctx, x, y, s, t, a=1.0, flip=1):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s * flip, s)
    wob = 0.06 * math.sin(t * 5 + x)
    ctx.rotate(wob)
    ctx.save(); ctx.scale(1, 0.25); circle(ctx, 0, 0, 40, C['dark'], 0.3 * a); ctx.restore()
    ctx.save(); ctx.translate(0, -60); ctx.scale(0.8, 1.15); circle(ctx, 0, 0, 52, '#1a2140', a); ctx.restore()
    ctx.save(); ctx.translate(4, -52); ctx.scale(0.6, 0.95); circle(ctx, 0, 0, 48, '#ffffff', a); ctx.restore()
    circle(ctx, 10, -112, 7, '#ffffff', a); circle(ctx, 12, -112, 3.5, C['dark'], a)
    ctx.move_to(22, -104); ctx.line_to(46, -98); ctx.line_to(22, -94); ctx.close_path(); src(ctx, C['orange'], a); ctx.fill()
    for fx in (-14, 14):
        ctx.save(); ctx.translate(fx, -2); ctx.scale(1, 0.4); circle(ctx, 0, 0, 14, C['orange'], a); ctx.restore()
    ctx.restore()


def price_tag(ctx, x, y, s, txt, sub, a=1.0, rot=-0.08):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-330, -120); ctx.line_to(260, -120); ctx.line_to(360, 0); ctx.line_to(260, 120); ctx.line_to(-330, 120); ctx.close_path()
    src(ctx, C['yellow'], a); ctx.fill()
    circle(ctx, 270, 0, 18, '#05081a', a)
    rich(ctx, [(txt, C['dark'])], -30, -20, 92, a, pop=False, shadow=False, maxw=560)
    rich(ctx, [(sub, '#5a4a10')], -30, 70, 36, a, pop=False, shadow=False, w='normal', maxw=560)
    ctx.restore()


def icefin(ctx, x, y, s, t, a=1.0):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(130, 0); ctx.line_to(700, -160); ctx.line_to(700, 160); ctx.close_path()
    g = cairo.LinearGradient(130, 0, 700, 0); g.add_color_stop_rgba(0, 1, 1, 0.8, 0.35 * a); g.add_color_stop_rgba(1, 1, 1, 0.8, 0)
    ctx.set_source(g); ctx.fill()
    rrect(ctx, -160, -34, 300, 68, 34); src(ctx, '#ffd23f', a); ctx.fill()
    rrect(ctx, -160, -34, 300, 22, 11); ctx.set_source_rgba(1, 1, 1, 0.3 * a); ctx.fill()
    ctx.move_to(-150, 0); ctx.line_to(-200, -46); ctx.line_to(-200, 46); ctx.close_path(); src(ctx, '#e0a020', a); ctx.fill()
    circle(ctx, 125, 0, 18, '#fff8c0', a)
    for k in range(3): rrect(ctx, -90 + k * 60, -6, 30, 12, 6); src(ctx, '#3a2a1a', 0.6 * a); ctx.fill()
    ctx.restore()


def thermometer(ctx, x, y, s, level, a=1.0, col=None):
    if s <= 1e-3 or a <= 0: return
    col = col or C['red']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -26, -200, 52, 220, 26); src(ctx, '#f4f6ff', a); ctx.fill()
    circle(ctx, 0, 40, 48, '#f4f6ff', a); circle(ctx, 0, 40, 34, col, a)
    hh = 180 * level
    rrect(ctx, -12, 20 - hh, 24, hh + 10, 12); src(ctx, col, a); ctx.fill()
    ctx.restore()


def turbine(ctx, x, y, s, t, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-8, 0); ctx.line_to(-4, -260); ctx.line_to(4, -260); ctx.line_to(8, 0); ctx.close_path(); src(ctx, '#e8ecff', a); ctx.fill()
    ctx.save(); ctx.translate(0, -260); ctx.rotate(t * 1.4)
    for k in range(3):
        ctx.save(); ctx.rotate(k * 2 * math.pi / 3)
        ctx.move_to(0, 0); ctx.curve_to(14, -40, 10, -120, 0, -150); ctx.curve_to(-6, -120, -8, -40, 0, 0); src(ctx, '#ffffff', a); ctx.fill()
        ctx.restore()
    circle(ctx, 0, 0, 10, '#c9d2ee', a); ctx.restore(); ctx.restore()


def solar_panel(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-100, -20); ctx.line_to(80, -70); ctx.line_to(110, 10); ctx.line_to(-70, 60); ctx.close_path(); src(ctx, '#2d6be0', a); ctx.fill()
    for k in range(1, 4):
        ctx.move_to(lerp(-100, 80, k / 4), lerp(-20, -70, k / 4)); ctx.line_to(lerp(-70, 110, k / 4), lerp(60, 10, k / 4))
    ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.5 * a); ctx.stroke()
    ctx.rectangle(-6, 40, 12, 60); src(ctx, '#9aaad6', a); ctx.fill()
    ctx.restore()


def warning_sign(ctx, x, y, s, a=1.0, t=0.0):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    glow(ctx, 0, 0, 260, C['yellow'], 0.35 * a * (0.8 + 0.2 * math.sin(t * 4)))
    ctx.new_path(); ctx.move_to(0, -120); ctx.line_to(120, 90); ctx.line_to(-120, 90); ctx.close_path()
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_line_width(30); src(ctx, C['yellow'], a); ctx.stroke_preserve(); ctx.fill()
    rrect(ctx, -11, -50, 22, 90, 11); src(ctx, C['dark'], a); ctx.fill()
    circle(ctx, 0, 64, 13, C['dark'], a)
    ctx.restore()
