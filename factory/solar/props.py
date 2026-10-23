"""Drawing props for the solar-storm video."""
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'long'))
from base import *
from render import planet

SUN_COL = ['#fff6c8', '#ffd23f', '#ff9a3d', '#ff5a3d']
random.seed(101)
GRAN = [(random.uniform(0, 6.283), random.uniform(0, 0.95), random.uniform(0.06, 0.16), random.uniform(0.3, 1.0),
         random.uniform(-0.2, 0.2)) for _ in range(70)]
SPOTS = [(0.35, -0.2, 0.07), (0.42, -0.12, 0.045), (-0.3, 0.25, 0.06), (-0.22, 0.31, 0.035), (0.1, 0.45, 0.04)]


def sun(ctx, cx, cy, r, t, flare=0.0, loops=1.0, flare_pos=(0.35, -0.18), spots=1.0, glow_a=1.0):
    glow(ctx, cx, cy, r * 2.6, '#ff9a3d', 0.55 * glow_a)
    glow(ctx, cx, cy, r * 1.6, '#ffd23f', 0.5 * glow_a)
    ctx.save(); ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
    g = cairo.RadialGradient(cx - r * 0.2, cy - r * 0.2, r * 0.1, cx, cy, r)
    g.add_color_stop_rgba(0, *hexc(SUN_COL[0])); g.add_color_stop_rgba(0.45, *hexc(SUN_COL[1]))
    g.add_color_stop_rgba(0.85, *hexc(SUN_COL[2])); g.add_color_stop_rgba(1, *hexc(SUN_COL[3]))
    ctx.set_source(g); ctx.paint()
    for (a, d, s, br, sp) in GRAN:
        aa = a + t * sp * 0.3
        x = cx + r * d * math.cos(aa); y = cy + r * d * math.sin(aa)
        rr = r * s * (0.85 + 0.15 * math.sin(t * 1.5 + a * 3))
        circle(ctx, x, y, rr, '#ffffff' if br > 0.7 else '#ff7a2a', 0.12 if br > 0.7 else 0.18)
    if spots > 0:
        for (sx, sy, sr) in SPOTS:
            circle(ctx, cx + sx * r, cy + sy * r, sr * r * 1.5, '#e0602a', 0.6 * spots)
            circle(ctx, cx + sx * r, cy + sy * r, sr * r, '#6a2a1a', 0.9 * spots)
    if flare > 0:
        fx, fy = cx + flare_pos[0] * r, cy + flare_pos[1] * r
        for k, (ox, oy) in enumerate(((0, 0), (0.08, 0.05))):
            glow(ctx, fx + ox * r, fy + oy * r, r * 0.35 * (0.6 + flare), '#ffffff', 0.9 * flare)
            circle(ctx, fx + ox * r, fy + oy * r, r * 0.04 * (0.5 + flare), '#ffffff', flare)
    ctx.restore()
    if loops > 0:
        for k in range(5):
            a = -2.2 + k * 0.55 + 0.05 * math.sin(t + k)
            x0, y0 = cx + r * math.cos(a - 0.12), cy + r * math.sin(a - 0.12)
            x1, y1 = cx + r * math.cos(a + 0.12), cy + r * math.sin(a + 0.12)
            h = r * (0.25 + 0.08 * math.sin(t * 0.8 + k * 1.7))
            mx, my = cx + (r + h) * math.cos(a), cy + (r + h) * math.sin(a)
            ctx.move_to(x0, y0); ctx.curve_to(mx + (x0 - x1) * 0.4, my + (y0 - y1) * 0.4, mx - (x0 - x1) * 0.4,
                                              my - (y0 - y1) * 0.4, x1, y1)
            ctx.set_line_width(r * 0.035); src(ctx, '#ff7a3d', 0.75 * loops); ctx.stroke()


random.seed(202)
CME_P = [(random.uniform(-1, 1), random.gauss(0, 0.45), random.uniform(0.4, 1.0), random.uniform(3, 9)) for _ in range(260)]


def cme(ctx, x0, y0, p, length, ang=0.0, spread=0.5, a=1.0, col='#ffb34a'):
    """particle cloud flying from (x0,y0) along angle ang; p in [0,1] progress, front at p*length."""
    if p <= 0: return
    for (u, v, sp, sz) in CME_P:
        d = length * p * sp * (0.75 + 0.25 * (u + 1) / 2)
        w = v * spread * d * 0.9
        x = x0 + d * math.cos(ang) - w * math.sin(ang)
        y = y0 + d * math.sin(ang) + w * math.cos(ang)
        circle(ctx, x, y, sz * (0.6 + p * 0.6), col, a * (0.35 + 0.5 * sp))
    fx, fy = x0 + length * p * 0.9 * math.cos(ang), y0 + length * p * 0.9 * math.sin(ang)
    glow(ctx, fx, fy, 160 + 200 * p, col, 0.35 * a)


def earth(ctx, cx, cy, r, t, night=0.0):
    planet(ctx, cx, cy, r, t * 0.15)
    if night > 0:
        ctx.save(); ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.clip()
        g = cairo.LinearGradient(cx - r, 0, cx + r, 0)
        g.add_color_stop_rgba(0, 0.02, 0.03, 0.12, 0); g.add_color_stop_rgba(0.5, 0.02, 0.03, 0.12, 0.2 * night)
        g.add_color_stop_rgba(1, 0.02, 0.03, 0.12, 0.85 * night)
        ctx.set_source(g); ctx.paint(); ctx.restore()


def magnetosphere(ctx, cx, cy, r, t, squeeze=0.0, a=1.0, shake=0.0):
    for k in range(1, 6):
        rr = r * (1.25 + 0.38 * k)
        day = rr * (1 - 0.35 * squeeze)
        ctx.save(); ctx.translate(cx + shake * math.sin(t * 30 + k) * 6, cy)
        ctx.new_path()
        for i in range(0, 361, 6):
            th = math.radians(i)
            rx = day if math.cos(th) < 0 else rr * (1 + 0.9 * squeeze * math.cos(th) ** 2)
            x = rx * math.cos(th); y = rr * 0.72 * math.sin(th) * (1 - 0.15 * squeeze * (math.cos(th) < 0))
            (ctx.move_to if i == 0 else ctx.line_to)(x, y)
        ctx.close_path(); ctx.set_line_width(3); src(ctx, C['cyan'], (0.45 - 0.06 * k) * a); ctx.stroke()
        ctx.restore()


def aurora(ctx, x0, x1, ytop, ybot, t, a=1.0, cols=('#5ee38a', '#3ee0ff', '#ff4f81')):
    if a <= 0: return
    n = int((x1 - x0) / 14)
    for i in range(n):
        x = x0 + i * 14
        u = i / n
        wave = math.sin(u * 9 + t * 0.9) * 0.5 + math.sin(u * 23 - t * 1.4) * 0.25
        top = ytop + 60 * wave
        hh = (ybot - ytop) * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(u * 13 + t * 1.1)))
        col = cols[0] if (u * 3 + t * 0.1) % 1 < 0.75 else cols[1]
        g = cairo.LinearGradient(0, top, 0, top + hh)
        cr, cg, cb, _ = hexc(cols[2])
        g.add_color_stop_rgba(0, cr, cg, cb, 0); g.add_color_stop_rgba(0.25, cr, cg, cb, 0.25 * a)
        r_, g_, b_, _ = hexc(col)
        g.add_color_stop_rgba(0.6, r_, g_, b_, 0.55 * a); g.add_color_stop_rgba(1, r_, g_, b_, 0)
        ctx.rectangle(x, top, 14, hh); ctx.set_source(g); ctx.fill()


def pylon(ctx, x, base, s, col='#9aaad6', a=1.0):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    ctx.set_line_width(5); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    src(ctx, col, a)
    ctx.move_to(-50, 0); ctx.line_to(-10, -260); ctx.line_to(10, -260); ctx.line_to(50, 0)
    for y in range(-30, -250, -45):
        w = 50 - (-y) / 260 * 40
        ctx.move_to(-w, y); ctx.line_to(w, y - 40); ctx.move_to(w, y); ctx.line_to(-w, y - 40)
    ctx.move_to(-70, -200); ctx.line_to(70, -200); ctx.move_to(-55, -240); ctx.line_to(55, -240)
    ctx.stroke(); ctx.restore()


def wire_line(ctx, pts, t, a=1.0, current=0.0, col='#9aaad6', pulse_col=None):
    ctx.new_path()
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        ctx.move_to(x0, y0); ctx.curve_to(x0 + (x1 - x0) * 0.3, y0 + 40, x0 + (x1 - x0) * 0.7, y1 + 40, x1, y1)
    ctx.set_line_width(3); src(ctx, col, a); ctx.stroke()
    if current > 0:
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            for k in range(3):
                u = (t * 0.9 + k / 3 + i * 0.13) % 1
                x = lerp(x0, x1, u); y = lerp(y0, y1, u) + 40 * 4 * u * (1 - u) * 0.75
                glow(ctx, x, y, 30, pulse_col or C['yellow'], 0.7 * current)
                circle(ctx, x, y, 6, pulse_col or C['yellow'], current)


def transformer(ctx, x, y, s, heat=0.0, t=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if heat > 0: glow(ctx, 0, -90, 260, C['red'], 0.6 * heat * (0.8 + 0.2 * math.sin(t * 10)))
    body = lerp_col('#5a6ab8', '#ff5a3d', heat)
    for k in range(7):
        rrect(ctx, -150 + k * 44, -170, 22, 150, 8); src(ctx, shade(body, 0.75), a); ctx.fill()
    rrect(ctx, -110, -200, 220, 200, 22); src(ctx, body, a); ctx.fill()
    for k in range(3):
        rrect(ctx, -70 + k * 55, -260, 30, 70, 10); src(ctx, '#d4dcf2', a); ctx.fill()
        circle(ctx, -55 + k * 55, -262, 20, '#d4dcf2', a)
    rrect(ctx, -60, -130, 120, 60, 12); src(ctx, '#0f1640', a); ctx.fill()
    ctx.move_to(-10, -125); ctx.line_to(10, -105); ctx.line_to(-6, -100); ctx.line_to(12, -75)
    ctx.set_line_width(6); src(ctx, C['yellow'], a); ctx.stroke()
    ctx.restore()


def satellite(ctx, x, y, s, rot=0.0, col='#d4dcf2', panel='#3ee0ff', a=1.0, glitch_=0.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    for sx in (-1, 1):
        rrect(ctx, sx * 40 - (60 if sx < 0 else 0), -18, 60, 36, 4); src(ctx, panel if glitch_ < 0.5 else C['red'], a); ctx.fill()
        for k in range(1, 4):
            ctx.move_to(sx * 40 - (60 if sx < 0 else 0) + k * 15, -18); ctx.line_to(sx * 40 - (60 if sx < 0 else 0) + k * 15, 18)
        ctx.set_line_width(2); ctx.set_source_rgba(0, 0, 0.2, 0.4 * a); ctx.stroke()
    rrect(ctx, -26, -24, 52, 48, 10); src(ctx, col, a); ctx.fill()
    circle(ctx, 0, -32, 8, col, a)
    if glitch_ > 0.5 and int(t * 10) % 2 == 0:
        circle(ctx, 0, 0, 10, C['red'], a)
    ctx.restore()


def tractor(ctx, x, y, s, rot=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -70, -60, 110, 50, 10); src(ctx, '#5ee38a', a); ctx.fill()
    rrect(ctx, 0, -110, 60, 60, 10); src(ctx, '#2f8f58', a); ctx.fill()
    rrect(ctx, 10, -100, 40, 34, 6); src(ctx, '#bfe9ff', a); ctx.fill()
    circle(ctx, 30, -10, 34, '#232f6e', a); circle(ctx, 30, -10, 14, '#9aaad6', a)
    circle(ctx, -50, -5, 22, '#232f6e', a); circle(ctx, -50, -5, 9, '#9aaad6', a)
    ctx.restore()


def plane(ctx, x, y, s, rot=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(-60, 0); ctx.curve_to(-60, -10, 50, -12, 64, 0); ctx.curve_to(50, 12, -60, 10, -60, 0); src(ctx, C['white'], a); ctx.fill()
    ctx.move_to(-5, -4); ctx.line_to(-30, -50); ctx.line_to(-16, -50); ctx.line_to(20, -4); ctx.close_path(); ctx.fill()
    ctx.move_to(-5, 4); ctx.line_to(-30, 50); ctx.line_to(-16, 50); ctx.line_to(20, 4); ctx.close_path(); ctx.fill()
    ctx.move_to(-50, -3); ctx.line_to(-62, -24); ctx.line_to(-54, -24); ctx.line_to(-40, -3); ctx.close_path(); ctx.fill()
    ctx.restore()


def telegraph(ctx, x, y, s, t, press=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -160, -20, 320, 40, 10); src(ctx, '#8c6a45', a); ctx.fill()
    rrect(ctx, -120, -60, 120, 40, 8); src(ctx, '#b0875a', a); ctx.fill()
    ctx.save(); ctx.translate(40, -40); ctx.rotate(-0.15 + 0.15 * press)
    rrect(ctx, 0, -10, 110, 16, 6); src(ctx, '#c9a26a', a); ctx.fill(); circle(ctx, 110, -2, 16, '#2a1f4f', a); ctx.restore()
    circle(ctx, -60, -60, 26, '#d9b25a', a); circle(ctx, -60, -60, 12, '#6b4f33', a)
    ctx.restore()


def spark(ctx, x, y, r, t, a=1.0, col=None, seed=0):
    rnd = random.Random(int(t * 24) + seed)
    glow(ctx, x, y, r * 1.4, col or C['yellow'], 0.7 * a)
    for k in range(7):
        ang = rnd.uniform(0, 6.283); L = rnd.uniform(0.4, 1.0) * r
        ctx.move_to(x, y)
        mx, my = x + L * 0.5 * math.cos(ang) + rnd.uniform(-8, 8), y + L * 0.5 * math.sin(ang) + rnd.uniform(-8, 8)
        ctx.line_to(mx, my); ctx.line_to(x + L * math.cos(ang), y + L * math.sin(ang))
    ctx.set_line_width(4); src(ctx, '#fff3c8', a); ctx.stroke()


def bolt(ctx, x, y, s, col=None, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(10, -60); ctx.line_to(-25, 5); ctx.line_to(0, 5); ctx.line_to(-12, 60); ctx.line_to(28, -10); ctx.line_to(2, -10)
    ctx.line_to(18, -60); ctx.close_path(); src(ctx, col or C['yellow'], a); ctx.fill(); ctx.restore()


def icon_tap(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -50, -30, 90, 26, 10); src(ctx, C['white'], a); ctx.fill()
    rrect(ctx, 20, -30, 24, 50, 8); ctx.fill(); rrect(ctx, -20, -52, 14, 26, 5); ctx.fill(); rrect(ctx, -36, -58, 46, 12, 6); ctx.fill()
    ctx.move_to(32, 30); ctx.curve_to(18, 50, 22, 62, 32, 62); ctx.curve_to(42, 62, 46, 50, 32, 30); src(ctx, C['cyan'], a); ctx.fill()
    ctx.restore()


def icon_fuel(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -36, -55, 56, 110, 10); src(ctx, C['white'], a); ctx.fill()
    rrect(ctx, -26, -45, 36, 26, 5); src(ctx, '#20307e', a); ctx.fill()
    ctx.move_to(20, -30); ctx.line_to(42, -10); ctx.line_to(42, 30); ctx.line_to(30, 40); ctx.set_line_width(8); src(ctx, C['white'], a); ctx.stroke()
    ctx.restore()


def icon_card(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -55, -36, 110, 72, 12); src(ctx, C['white'], a); ctx.fill()
    ctx.rectangle(-55, -20, 110, 16); src(ctx, '#20307e', a); ctx.fill()
    rrect(ctx, -40, 8, 30, 16, 4); src(ctx, C['yellow'], a); ctx.fill(); ctx.restore()


def icon_tower(ctx, x, y, s, t, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-30, 60); ctx.line_to(0, -40); ctx.line_to(30, 60); ctx.move_to(-18, 20); ctx.line_to(18, 20)
    ctx.set_line_width(8); src(ctx, C['white'], a); ctx.stroke()
    circle(ctx, 0, -44, 10, C['white'], a)
    for k in (1, 2):
        ctx.new_path(); ctx.arc(0, -44, 22 * k, -2.4, -0.74); ctx.set_line_width(6); src(ctx, C['white'], a); ctx.stroke()
        ctx.new_path(); ctx.arc(0, -44, 22 * k, 0.74 - math.pi, 2.4 - math.pi); ctx.stroke()
    ctx.restore()


def icon_med(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -40, -50, 80, 100, 14); src(ctx, C['white'], a); ctx.fill()
    rrect(ctx, -10, -30, 20, 60, 4); src(ctx, C['red'], a); ctx.fill(); rrect(ctx, -30, -10, 60, 20, 4); ctx.fill()
    ctx.restore()


def x_mark(ctx, x, y, r, p, col=None):
    if p <= 0: return
    ctx.set_line_width(14); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, col or C['red'])
    k1 = clamp(p * 2); k2 = clamp(p * 2 - 1)
    ctx.move_to(x - r, y - r); ctx.line_to(x - r + 2 * r * k1, y - r + 2 * r * k1); ctx.stroke()
    if k2 > 0:
        ctx.move_to(x + r, y - r); ctx.line_to(x + r - 2 * r * k2, y - r + 2 * r * k2); ctx.stroke()


def city(ctx, base, t, lights=1.0, seed=5, a=1.0, x0=0, x1=W, dark_wave=None):
    rnd = random.Random(seed); x = x0 - 20
    while x < x1 + 40:
        w_ = rnd.uniform(70, 160); h_ = rnd.uniform(120, 420)
        rrect(ctx, x, base - h_, w_, h_ + 40, 6); src(ctx, '#18245e' if rnd.random() > 0.5 else '#1d2c6e', a); ctx.fill()
        r2 = random.Random(int(x * 7))
        for wy in range(int(base - h_ + 20), int(base - 8), 30):
            for wx in range(int(x + 12), int(x + w_ - 16), 26):
                if r2.random() < 0.42:
                    lv = lights if dark_wave is None else clamp((x - dark_wave) / 160)
                    if lv > 0.02:
                        ctx.rectangle(wx, wy, 12, 16); src(ctx, C['yellow'], 0.6 * lv * a); ctx.fill()
        x += w_ + rnd.uniform(4, 16)
