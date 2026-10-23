"""Landscape (1920x1080) drawing helpers shared by all long-form scenes."""
import cairo, math, random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from render import (C, hexc, clamp, prog, eo, ss, eback, lerp, src, rrect, circle, glow, font, rich, person,
                    laptop, chip_icon, card_icon, code_icon)
from deepfake import (face, wire, glitched, pill, bubble, robot, big_eye, phone_icon, lock_icon, glass_icon,
                      LOOKS, ring_timer, shade, lerp_col)

W, H, FPS = 1920, 1080, 30
import render as _r, deepfake as _d
_hex0 = _r.hexc
def hexc(h, a=1.0):
    if isinstance(h, tuple): return (h[0], h[1], h[2], h[3] * a if len(h) > 3 else a)
    return _hex0(h, a)
_r.hexc = hexc; _d.hexc = hexc

random.seed(11)
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1.2, 3.4), random.uniform(0, 6.28),
          random.uniform(0.6, 2.2)) for _ in range(170)]


def bg(ctx, t, top=C['navy'], bot=C['navy2'], glow_col=C['purple'], gx=960, gy=620, gr=1300, stars=1.0,
       drift=0.0):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hexc(top)); g.add_color_stop_rgba(1, *hexc(bot))
    ctx.set_source(g); ctx.paint()
    glow(ctx, gx, gy, gr, glow_col, 0.55)
    if stars > 0:
        for (x, y, r, ph, sp) in STARS:
            xx = (x - drift * sp) % W
            a = 0.3 + 0.45 * (0.5 + 0.5 * math.sin(t * sp * 2.2 + ph))
            circle(ctx, xx, y, r, C['white'], a * stars)


def vignette(ctx):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.45, W / 2, H / 2, W * 0.62)
    g.add_color_stop_rgba(0, 0, 0, 0.05, 0); g.add_color_stop_rgba(1, 0, 0, 0.05, 0.5)
    ctx.set_source(g); ctx.paint()


def source_line(ctx, txt, a=1.0, y=1045):
    if a <= 0: return
    font(ctx, 22, 'normal')
    w = ctx.text_extents(txt).x_advance
    ctx.move_to(W - 40 - w, y); src(ctx, C['grey'], 0.85 * a); ctx.show_text(txt)


def title(ctx, parts, y, size, p, maxw=1700, **kw):
    rich(ctx, parts, W / 2, y, size, p, maxw=maxw, **kw)


def hills(ctx, base_y, col, amp=40, freq=1.0, phase=0.0, a=1.0):
    ctx.new_path(); ctx.move_to(0, H)
    for x in range(0, W + 41, 40):
        y = base_y - amp * (math.sin(x / 300 * freq + phase) * 0.6 + math.sin(x / 130 * freq + phase * 1.7) * 0.4)
        ctx.line_to(x, y)
    ctx.line_to(W, H); ctx.close_path(); src(ctx, col, a); ctx.fill()


def horizon(ctx, cy, r, col, edge=None):
    ctx.new_path(); ctx.arc(W / 2, cy + r, r, 0, 2 * math.pi); src(ctx, col); ctx.fill()
    if edge:
        ctx.new_path(); ctx.arc(W / 2, cy + r, r, math.pi * 1.1, math.pi * 1.9)
        ctx.set_line_width(6); src(ctx, edge, 0.6); ctx.stroke()


def pixelate_region(ctx, draw, x, y, w, h, block, alpha=1.0):
    """Draw `draw(c)` (global coords) into a w x h region, mosaic with `block` px cells."""
    tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w), int(h))
    tc = cairo.Context(tmp); tc.translate(-x, -y); draw(tc); tmp.flush()
    if block <= 1.05:
        ctx.set_source_surface(tmp, x, y); ctx.paint_with_alpha(alpha); return
    sw, sh = max(1, int(w / block)), max(1, int(h / block))
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    sc = cairo.Context(small); sc.scale(sw / w, sh / h); sc.set_source_surface(tmp, 0, 0)
    sc.get_source().set_filter(cairo.FILTER_GOOD); sc.paint()
    ctx.save(); ctx.translate(x, y); ctx.scale(w / sw, h / sh); ctx.set_source_surface(small, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_NEAREST); ctx.paint_with_alpha(alpha); ctx.restore()


def card(ctx, x, y, w, h, fill='#20307e', r=36, stroke=True):
    rrect(ctx, x, y, w, h, r); src(ctx, fill); ctx.fill()
    if stroke:
        rrect(ctx, x, y, w, h, r); ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke()


def pop_scale(ctx, cx, cy, p, fn, s=1.6):
    if p <= 0: return
    k = eback(p, s)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy); fn(); ctx.restore()


def text_left(ctx, parts, x, y, size, p=1.0, maxw=900, w='bold', pop=False):
    rich(ctx, parts, x, y, size, p, maxw=maxw, w=w, align='left', pop=pop)


def robot2(ctx, x, y, s, body, accent, kind, t, talk=0.0, look=0.0, a=1.0, arm=0.0):
    """Friendly boxy robot. kind: 'forger' (beret + brush) or 'detective' (hat + magnifier)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.22); circle(ctx, 0, 0, 120, C['dark'], 0.35 * a); ctx.restore()
    for lx in (-45, 25):
        rrect(ctx, lx, -95, 22, 95, 11); src(ctx, shade(body, 0.7), a); ctx.fill()
    # arms
    for side in (-1, 1):
        ang = (0.25 + (arm if side == (1 if kind == 'forger' else -1) else 0)) * -side
        ctx.save(); ctx.translate(side * 82, -205); ctx.rotate(ang)
        rrect(ctx, -12, -8, 24, 105, 12); src(ctx, shade(body, 0.8), a); ctx.fill()
        hx, hy = 0, 100
        circle(ctx, hx, hy, 16, shade(body, 0.9), a)
        if side == (1 if kind == 'forger' else -1):
            if kind == 'forger':
                ctx.move_to(hx, hy); ctx.line_to(hx + 8, hy + 80); ctx.set_line_width(10); src(ctx, '#b07a4a', a)
                ctx.stroke(); circle(ctx, hx + 9, hy + 88, 12, accent, a)
            else:
                ctx.move_to(hx, hy); ctx.line_to(hx - 10, hy + 55); ctx.set_line_width(12); src(ctx, '#3a2a1a', a)
                ctx.stroke(); ctx.new_path(); ctx.arc(hx - 18, hy + 95, 40, 0, 2 * math.pi)
                ctx.set_source_rgba(0.7, 0.95, 1, 0.25 * a); ctx.fill_preserve(); ctx.set_line_width(10)
                src(ctx, '#d9b25a', a); ctx.stroke()
        ctx.restore()
    rrect(ctx, -85, -260, 170, 175, 46); src(ctx, body, a); ctx.fill()
    rrect(ctx, -85, -260, 170, 45, 22); ctx.set_source_rgba(1, 1, 1, 0.14 * a); ctx.fill()
    rrect(ctx, -40, -200, 80, 60, 14); src(ctx, '#0f1640', a); ctx.fill()
    circle(ctx, 0, -170, 14, accent, a)
    # head
    ctx.move_to(0, -262); ctx.line_to(0, -282); ctx.set_line_width(10); src(ctx, shade(body, 0.8), a); ctx.stroke()
    rrect(ctx, -105, -420, 210, 150, 50); src(ctx, body, a); ctx.fill()
    rrect(ctx, -82, -398, 164, 105, 34); src(ctx, '#0f1640', a); ctx.fill()
    for sx in (-1, 1):
        ex = sx * 36 + look * 12
        glow(ctx, ex, -352, 50, accent, 0.5 * a)
        blink = 0.15 if (t * 0.7 + (0.3 if kind == 'forger' else 0)) % 3.1 < 0.1 else 1.0
        ctx.save(); ctx.translate(ex, -352); ctx.scale(1, blink); circle(ctx, 0, 0, 15, accent, a); ctx.restore()
    for k in range(5):
        hh = 6 + 18 * talk * abs(math.sin(t * 14 + k * 1.3))
        rrect(ctx, -30 + k * 13, -312 - hh / 2, 7, hh, 3.5); src(ctx, accent, a); ctx.fill()
    if kind == 'forger':
        ctx.save(); ctx.translate(-20, -420); ctx.rotate(-0.25); ctx.scale(1, 0.42)
        circle(ctx, 0, 0, 92, C['pink'], a); ctx.restore()
        circle(ctx, -48, -452, 12, C['pink'], a)
    else:
        ctx.save(); ctx.translate(0, -418); ctx.scale(1, 0.22); circle(ctx, 0, 0, 140, '#7a5a3a', a); ctx.restore()
        rrect(ctx, -75, -485, 150, 72, 30); src(ctx, '#8c6a45', a); ctx.fill()
        ctx.rectangle(-75, -440, 150, 16); src(ctx, '#3a2a1a', a); ctx.fill()
    ctx.restore()


def wave_bars(ctx, x0, yc, n, sp, hmax, t, col, a=1.0, seed=0, grow=1.0, wbar=None):
    rnd = random.Random(seed)
    vals = [0.25 + 0.75 * abs(math.sin(i * 0.9 + seed) * math.cos(i * 0.37 + seed)) for i in range(n)]
    for i, v in enumerate(vals):
        if i / n > grow: break
        hh = 16 + hmax * v * (0.75 + 0.25 * math.sin(t * 8 + i))
        bw = wbar or sp * 0.6
        rrect(ctx, x0 + i * sp, yc - hh / 2, bw, hh, bw / 2); src(ctx, col, a); ctx.fill()


def phone(ctx, x, y, s, screen='#1b2a6e', a=1.0, ring=0.0, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if ring > 0:
        for k in range(3):
            ph = (t * 1.4 + k / 3) % 1
            ctx.new_path(); ctx.arc(0, 0, 140 + ph * 160, -2.4, -0.74); ctx.set_line_width(10)
            src(ctx, C['yellow'], (1 - ph) * ring * a); ctx.stroke()
        ctx.rotate(0.06 * math.sin(t * 40) * ring)
    rrect(ctx, -95, -185, 190, 370, 34); src(ctx, '#e8ecff', a); ctx.fill()
    rrect(ctx, -82, -165, 164, 330, 22); src(ctx, screen, a); ctx.fill()
    rrect(ctx, -30, -178, 60, 8, 4); src(ctx, '#9aa6cf', a); ctx.fill()
    ctx.restore()


def money(ctx, x, y, s, rot=0.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    rrect(ctx, -60, -32, 120, 64, 10); src(ctx, '#57c785', a); ctx.fill()
    rrect(ctx, -50, -22, 100, 44, 8); ctx.set_line_width(4); src(ctx, '#2f8f58', a); ctx.stroke()
    circle(ctx, 0, 0, 15, '#2f8f58', a)
    ctx.restore()


def coin(ctx, x, y, r, a=1.0):
    circle(ctx, x, y, r, '#f2b632', a); circle(ctx, x, y, r * 0.72, C['yellow'], a)
    ctx.new_path(); ctx.arc(x - r * 0.25, y - r * 0.25, r * 0.35, 3.4, 4.9); ctx.set_line_width(r * 0.12)
    ctx.set_source_rgba(1, 1, 1, 0.6 * a); ctx.stroke()


def house(ctx, x, y, s, col, a=1.0, lit=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-40, -50, 80, 50); src(ctx, col, a); ctx.fill()
    ctx.move_to(-50, -48); ctx.line_to(0, -92); ctx.line_to(50, -48); ctx.close_path(); src(ctx, shade(col, 0.7), a)
    ctx.fill()
    rrect(ctx, -26, -38, 20, 18, 3); src(ctx, C['yellow'] if lit else '#33458f', a); ctx.fill()
    rrect(ctx, 8, -30, 18, 30, 3); src(ctx, '#2a1f4f', a); ctx.fill()
    ctx.restore()


def stamp(ctx, x, y, txt, col, p, rot=-0.18, size=110):
    if p <= 0: return
    sc = 1 + 1.6 * (1 - eo(p))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    font(ctx, size); w = ctx.text_extents(txt).x_advance
    rrect(ctx, -w / 2 - 30, -size * 0.75, w + 60, size * 1.3, 18); ctx.set_line_width(12); src(ctx, col, clamp(p * 3))
    ctx.stroke()
    ctx.move_to(-w / 2, size * 0.36); src(ctx, col, clamp(p * 3)); ctx.show_text(txt)
    ctx.restore()


def counter_text(v, fmt='{:,}'):
    return fmt.format(int(round(v)))
