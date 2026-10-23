import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'aijobs'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solar'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'long'))
from props_ai import *
from render import bulb

GOLD = '#f2b632'
GOLD2 = '#ffd98a'
COPPER = '#d98a4a'
BTC = '#f7931a'
Q = '#b28cff'          # quantum purple


def padlock(ctx, x, y, s, open_=0.0, body=None, a=1.0, shackle=None, lattice=False, t=0.0):
    """Padlock centred on its body. open_ 0..1 lifts + swings the shackle."""
    if s <= 1e-3 or a <= 0: return
    body = body or C['yellow']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # shackle
    lift = 34 * ss(clamp(open_ * 2)); swing = 0.9 * ss(clamp(open_ * 2 - 1))
    ctx.save(); ctx.translate(46, -40 - lift); ctx.rotate(-swing); ctx.translate(-46, 0)
    ctx.new_path(); ctx.arc(0, -40, 46, math.pi, 2 * math.pi)
    ctx.move_to(-46, -40); ctx.line_to(-46, 10); ctx.move_to(46, -40); ctx.line_to(46, 10)
    ctx.set_line_width(22); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, shackle or '#c9d2ee', a); ctx.stroke()
    ctx.restore()
    rrect(ctx, -78, -48, 156, 128, 26); src(ctx, body, a); ctx.fill()
    rrect(ctx, -78, -48, 156, 34, 17); ctx.set_source_rgba(1, 1, 1, 0.22 * a); ctx.fill()
    if lattice:
        ctx.save(); rrect(ctx, -78, -48, 156, 128, 26); ctx.clip()
        for i in range(-3, 4):
            for j in range(-2, 4):
                px, py = i * 26 + (j % 2) * 13, j * 24 + 6
                circle(ctx, px, py, 3.6, '#ffffff', 0.55 * a * (0.6 + 0.4 * math.sin(t * 3 + i + j)))
        ctx.restore()
    circle(ctx, 0, 8, 14, C['dark'], 0.85 * a)
    rrect(ctx, -6, 10, 12, 32, 5); src(ctx, C['dark'], 0.85 * a); ctx.fill()
    ctx.restore()


def key(ctx, x, y, s, rot=0.0, col=None, a=1.0):
    if s <= 1e-3 or a <= 0: return
    col = col or GOLD
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(-60, 0, 34, 0, 2 * math.pi); ctx.arc_negative(-60, 0, 14, 2 * math.pi, 0)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); src(ctx, col, a); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    rrect(ctx, -30, -9, 110, 18, 6); ctx.fill()
    for bx, bh in ((50, 26), (68, 18)):
        ctx.rectangle(bx, 4, 12, bh); ctx.fill()
    ctx.restore()


def qcomputer(ctx, x, y, s, t, a=1.0, glow_a=1.0, cold=0.0):
    """Dilution-fridge 'chandelier' hanging from y (top)."""
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    glow(ctx, 0, 330, 420, Q, 0.45 * glow_a * a)
    glow(ctx, 0, 520, 200, C['cyan'], (0.35 + 0.15 * math.sin(t * 4)) * glow_a * a)
    levels = [(0, 170), (110, 150), (215, 128), (315, 104), (405, 80), (485, 56)]
    # rods
    for i in range(len(levels) - 1):
        y0, r0 = levels[i]; y1, r1 = levels[i + 1]
        for f in (-0.72, -0.25, 0.25, 0.72):
            ctx.move_to(f * r0, y0); ctx.line_to(f * r1, y1)
        ctx.set_line_width(8); src(ctx, '#c08a3a', a); ctx.stroke()
    # coiled cables
    for k, col in enumerate((COPPER, '#e0b070', '#c87a3a')):
        ctx.new_path()
        for j in range(0, 61):
            yy = 20 + j * 7.8
            xx = -40 + k * 40 + 18 * math.sin(j * 0.9 + k + t * 1.5) * (1 - j / 80)
            if j == 0: ctx.move_to(xx, yy)
            else: ctx.line_to(xx, yy)
        ctx.set_line_width(5); src(ctx, col, 0.9 * a); ctx.stroke()
    for (yy, r) in levels:
        ctx.save(); ctx.translate(0, yy); ctx.scale(1, 0.24)
        circle(ctx, 0, 6, r, '#a8701f', a); circle(ctx, 0, 0, r, GOLD, a)
        ctx.new_path(); ctx.arc(0, 0, r * 0.75, math.pi * 1.1, math.pi * 1.6); ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.35 * a); ctx.stroke()
        ctx.restore()
    # chip at the bottom
    rrect(ctx, -34, 500, 68, 46, 8); src(ctx, '#2a2f6a', a); ctx.fill()
    rrect(ctx, -22, 508, 44, 30, 5); src(ctx, C['cyan'], (0.6 + 0.4 * math.sin(t * 6)) * a); ctx.fill()
    # top plate
    rrect(ctx, -200, -40, 400, 40, 10); src(ctx, '#6b7fb8', a); ctx.fill()
    if cold > 0:
        for k in range(10):
            ph = (t * 0.4 + k * 0.1) % 1
            circle(ctx, -150 + k * 32, 40 + ph * 480, 4, '#dff6ff', cold * (1 - ph) * a)
    ctx.restore()


def bloch(ctx, x, y, r, t, a=1.0, spin=1.0, col=None):
    if r <= 1 or a <= 0: return
    col = col or Q
    glow(ctx, x, y, r * 1.8, col, 0.35 * a)
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.35, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, *hexc('#f0e6ff', 0.95 * a)); g.add_color_stop_rgba(1, *hexc(col, 0.85 * a))
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.translate(x, y); ctx.scale(1, 0.3); ctx.new_path(); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
    ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.6 * a); ctx.stroke()
    ctx.move_to(x, y - r); ctx.line_to(x, y + r); ctx.set_line_width(2); ctx.set_source_rgba(1, 1, 1, 0.4 * a); ctx.stroke()
    th = 0.9 + 0.5 * math.sin(t * 1.3 * spin); ph = t * 2.2 * spin
    ex = x + r * 0.92 * math.sin(th) * math.cos(ph); ey = y - r * 0.92 * math.cos(th) + r * 0.28 * math.sin(th) * math.sin(ph)
    ctx.move_to(x, y); ctx.line_to(ex, ey); ctx.set_line_width(7); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['yellow'], a); ctx.stroke()
    circle(ctx, ex, ey, 11, C['yellow'], a)
    rich(ctx, [('|0>', C['white'])], x, y - r - 30, 30, a, pop=False)
    rich(ctx, [('|1>', C['white'])], x, y + r + 34, 30, a, pop=False)


def bit_switch(ctx, x, y, s, val, a=1.0):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -60, -110, 120, 220, 60); src(ctx, '#1d2c6e', a); ctx.fill()
    yy = lerp(50, -50, val)
    circle(ctx, 0, yy, 48, C['yellow'] if val > 0.5 else C['grey'], a)
    rich(ctx, [('1' if val > 0.5 else '0', C['dark'])], 0, yy, 56, a, pop=False, shadow=False)
    ctx.restore()


def btc_coin(ctx, x, y, r, a=1.0, rot=0.0, sq=1.0, col=None):
    if r <= 1 or a <= 0: return
    col = col or BTC
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sq, 1)
    circle(ctx, 0, r * 0.06, r, shade(col, 0.72), a)
    circle(ctx, 0, 0, r, col, a); circle(ctx, 0, 0, r * 0.8, shade(col, 1.08) if False else '#ffa940', a)
    # B with bars
    k = r / 100
    ctx.set_line_width(13 * k); src(ctx, '#ffffff', a); ctx.set_line_cap(cairo.LINE_CAP_BUTT)
    for bx in (-12, 8):
        ctx.move_to(bx * k, -62 * k); ctx.line_to(bx * k, -44 * k); ctx.move_to(bx * k, 44 * k); ctx.line_to(bx * k, 62 * k)
    ctx.stroke()
    ctx.new_path(); ctx.move_to(-26 * k, -44 * k); ctx.line_to(10 * k, -44 * k)
    ctx.curve_to(40 * k, -44 * k, 40 * k, -4 * k, 10 * k, -4 * k); ctx.line_to(-26 * k, -4 * k)
    ctx.move_to(-26 * k, -4 * k); ctx.line_to(14 * k, -4 * k)
    ctx.curve_to(48 * k, -4 * k, 48 * k, 44 * k, 14 * k, 44 * k); ctx.line_to(-26 * k, 44 * k)
    ctx.move_to(-20 * k, -44 * k); ctx.line_to(-20 * k, 44 * k)
    ctx.set_line_width(14 * k); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    ctx.new_path(); ctx.arc(-r * 0.3, -r * 0.3, r * 0.35, 3.4, 4.9); ctx.set_line_width(r * 0.08); ctx.set_source_rgba(1, 1, 1, 0.5 * a); ctx.stroke()
    ctx.restore()


def hooded(ctx, x, y, s, a=1.0, t=0.0, eye=None, arm_r=0.3, arm_l=0.3):
    """Mysterious hooded figure (spy / attacker), same footprint as person()."""
    if s <= 1e-3 or a <= 0: return
    eye = eye or C['pink']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.25); circle(ctx, 0, 0, 60, C['dark'], 0.35 * a); ctx.restore()
    for lx in (-27, 3):
        rrect(ctx, lx, -72, 24, 72, 11); src(ctx, '#141a3a', a); ctx.fill()
    for side, ang in ((-1, arm_l), (1, arm_r)):
        ctx.save(); ctx.translate(side * 31, -136); ctx.rotate(-side * ang)
        rrect(ctx, -11, -6, 22, 76, 10); src(ctx, '#1c2250', a); ctx.fill(); ctx.restore()
    rrect(ctx, -44, -156, 88, 102, 30); src(ctx, '#232a5e', a); ctx.fill()
    ctx.new_path(); ctx.move_to(-46, -150); ctx.curve_to(-50, -240, 50, -240, 46, -150); ctx.close_path(); src(ctx, '#232a5e', a); ctx.fill()
    ctx.save(); ctx.translate(0, -186); ctx.scale(1, 1.12); circle(ctx, 0, 0, 28, '#05081a', a); ctx.restore()
    bl = 0.15 if (t * 0.7 + x * 0.003) % 3.1 < 0.12 else 1
    for sx in (-1, 1):
        ctx.save(); ctx.translate(sx * 10, -188); ctx.scale(1, bl); circle(ctx, 0, 0, 4.5, eye, a); ctx.restore()
    glow(ctx, 0, -188, 40, eye, 0.25 * a)
    ctx.restore()


def browser(ctx, x, y, w, h, url, lock=True, a=1.0, broken=0.0, body=None):
    if a <= 0: return
    rrect(ctx, x, y, w, h, 22); src(ctx, '#e8ecff', a); ctx.fill()
    rrect(ctx, x, y, w, 64, 22); src(ctx, '#c9d2ee', a); ctx.fill(); ctx.rectangle(x, y + 40, w, 24); ctx.fill()
    for k, col in enumerate((C['red'], C['yellow'], C['green'])): circle(ctx, x + 32 + k * 30, y + 32, 9, col, a)
    rrect(ctx, x + 130, y + 14, w - 160, 38, 19); src(ctx, '#ffffff', a); ctx.fill()
    lx = x + 156
    if lock:
        ctx.save(); ctx.translate(lx, y + 34); ctx.scale(0.42, 0.42)
        ctx.new_path(); ctx.arc(0, -10, 18, math.pi, 2 * math.pi); ctx.set_line_width(9)
        src(ctx, lerp_col(C['green'], C['red'], broken) if broken else C['green'], a); ctx.stroke()
        rrect(ctx, -26, -6, 52, 40, 8); ctx.fill(); ctx.restore()
    font(ctx, 24, 'normal'); ctx.move_to(lx + 26, y + 42); src(ctx, '#33458f', a); ctx.show_text(url)
    if body: body()


def chest(ctx, x, y, s, open_=0.0, a=1.0, fill=1.0, dust=0.0, t=0.0):
    if s <= 1e-3 or a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if fill > 0 and open_ > 0.05:
        for k in range(9):
            if k / 9 >= fill: break
            btc_coin(ctx, -90 + (k % 5) * 45, -112 + (k // 5) * 22 - 8 * math.sin(k), 30, a)
    rrect(ctx, -150, -110, 300, 150, 18); src(ctx, '#8c5a2a', a); ctx.fill()
    ctx.rectangle(-150, -60, 300, 16); src(ctx, '#c9973a', a); ctx.fill()
    for bx in (-110, 94): ctx.rectangle(bx, -110, 16, 150); ctx.fill()
    # lid
    ctx.save(); ctx.translate(0, -110); ctx.translate(-150, 0); ctx.rotate(-1.6 * ss(open_)); ctx.translate(150, 0)
    ctx.new_path(); ctx.move_to(-150, 0); ctx.line_to(-150, -40); ctx.curve_to(-150, -90, 150, -90, 150, -40); ctx.line_to(150, 0); ctx.close_path()
    src(ctx, '#a8692f', a); ctx.fill()
    ctx.rectangle(-8, -70, 16, 70); src(ctx, '#c9973a', a); ctx.fill()
    ctx.restore()
    if open_ < 0.1:
        rrect(ctx, -22, -126, 44, 40, 8); src(ctx, '#c9973a', a); ctx.fill(); circle(ctx, 0, -106, 7, C['dark'], a)
    if dust > 0:
        for k in range(14):
            rnd = random.Random(k * 13)
            circle(ctx, rnd.uniform(-160, 160), rnd.uniform(-160, 40), rnd.uniform(3, 7), '#c9c2b0', 0.5 * dust * a)
        ctx.new_path(); ctx.move_to(150, -110); ctx.line_to(200, -170); ctx.move_to(150, -60); ctx.line_to(205, -170)
        ctx.move_to(165, -128); ctx.line_to(185, -100); ctx.set_line_width(2); ctx.set_source_rgba(1, 1, 1, 0.35 * dust * a); ctx.stroke()
    ctx.restore()


def shield(ctx, x, y, s, col=None, a=1.0):
    if s <= 1e-3 or a <= 0: return
    col = col or C['green']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -110); ctx.curve_to(50, -80, 80, -84, 96, -86); ctx.curve_to(100, 10, 70, 80, 0, 116)
    ctx.curve_to(-70, 80, -100, 10, -96, -86); ctx.curve_to(-80, -84, -50, -80, 0, -110); ctx.close_path()
    src(ctx, col, a); ctx.fill()
    ctx.new_path(); ctx.move_to(-40, 4); ctx.line_to(-10, 36); ctx.line_to(46, -30)
    ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); src(ctx, C['white'], a); ctx.stroke()
    ctx.restore()


def calendar(ctx, x, y, s, top, big, col=None, a=1.0, big_col=None):
    if s <= 1e-3 or a <= 0: return
    col = col or C['red']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -130, -140, 260, 280, 26); src(ctx, '#f4f6ff', a); ctx.fill()
    rrect(ctx, -130, -140, 260, 80, 26); src(ctx, col, a); ctx.fill(); ctx.rectangle(-130, -90, 260, 30); ctx.fill()
    for rx in (-70, 70):
        rrect(ctx, rx - 9, -164, 18, 50, 9); src(ctx, '#9aaad6', a); ctx.fill()
    rich(ctx, [(top, C['white'])], 0, -98, 38, a, pop=False, shadow=False, maxw=230)
    rich(ctx, [(big, big_col or C['dark'])], 0, 40, 96, a, pop=False, shadow=False, maxw=230)
    ctx.restore()


def chip_grid(ctx, x, y, size, n_side, t, a=1.0, lit=1.0, col=None):
    """Square chip of side `size` with n_side x n_side qubit dots."""
    if size <= 2 or a <= 0: return
    col = col or C['cyan']
    rrect(ctx, x - size / 2, y - size / 2, size, size, size * 0.06); src(ctx, '#2a2f6a', a); ctx.fill()
    rrect(ctx, x - size / 2, y - size / 2, size, size, size * 0.06); ctx.set_line_width(max(1, size * 0.012)); src(ctx, GOLD, a); ctx.stroke()
    pad = size * 0.1; sp = (size - 2 * pad) / max(1, n_side - 1)
    rr = max(0.8, sp * 0.26)
    for i in range(n_side):
        for j in range(n_side):
            on = 0.5 + 0.5 * math.sin(t * 3 + i * 0.7 + j * 1.3)
            circle(ctx, x - size / 2 + pad + i * sp, y - size / 2 + pad + j * sp, rr, col, a * lit * (0.45 + 0.55 * on))


def molecule(ctx, x, y, s, t, a=1.0):
    if s <= 1e-3 or a <= 0: return
    atoms = [(0, 0, 34, C['pink']), (80, -40, 26, C['cyan']), (-80, -36, 26, C['cyan']), (10, 90, 26, C['yellow']),
             (150, 10, 18, C['white']), (-150, 16, 18, C['white'])]
    links = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 5)]
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.15 * math.sin(t * 0.8)); ctx.scale(s, s)
    for i, j in links:
        ctx.move_to(atoms[i][0], atoms[i][1]); ctx.line_to(atoms[j][0], atoms[j][1])
    ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.6 * a); ctx.stroke()
    for ax, ay, r, col in atoms:
        circle(ctx, ax, ay, r, col, a); circle(ctx, ax - r * 0.3, ay - r * 0.3, r * 0.3, '#ffffff', 0.4 * a)
    ctx.restore()


def hourglass(ctx, x, y, s, t, a=1.0, k=None):
    if s <= 1e-3 or a <= 0: return
    k = (t * 0.15) % 1 if k is None else k
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for yy in (-110, 98):
        rrect(ctx, -70, yy, 140, 12, 6); src(ctx, '#c9973a', a); ctx.fill()
    ctx.new_path(); ctx.move_to(-55, -98); ctx.curve_to(-55, -30, -8, -16, -6, 0); ctx.curve_to(-8, 16, -55, 30, -55, 98)
    ctx.line_to(55, 98); ctx.curve_to(55, 30, 8, 16, 6, 0); ctx.curve_to(8, -16, 55, -30, 55, -98); ctx.close_path()
    ctx.set_source_rgba(0.8, 0.9, 1, 0.25 * a); ctx.fill_preserve(); ctx.set_line_width(4); ctx.set_source_rgba(1, 1, 1, 0.6 * a); ctx.stroke()
    top = 1 - k
    ctx.new_path(); ctx.move_to(-45 * top, -10 - 70 * top); ctx.line_to(45 * top, -10 - 70 * top); ctx.line_to(0, -6); ctx.close_path()
    src(ctx, GOLD2, a); ctx.fill()
    ctx.new_path(); ctx.move_to(-50, 96); ctx.line_to(50, 96); ctx.line_to(0, 96 - 70 * k); ctx.close_path(); ctx.fill()
    ctx.move_to(0, -4); ctx.line_to(0, 94); ctx.set_line_width(3); src(ctx, GOLD2, a * (k < 0.98)); ctx.stroke()
    ctx.restore()


def packet(ctx, x, y, s, col=None, a=1.0, txt='01'):
    if s <= 1e-3 or a <= 0: return
    col = col or C['cyan']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -40, -26, 80, 52, 10); src(ctx, col, a); ctx.fill()
    rich(ctx, [(txt, C['dark'])], 0, 0, 26, a, pop=False, shadow=False)
    ctx.restore()


def ice_block(ctx, x, y, w, h, a=1.0):
    if a <= 0: return
    rrect(ctx, x - w / 2, y - h / 2, w, h, 22); src(ctx, '#bfefff', 0.55 * a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 22); ctx.set_line_width(6); src(ctx, '#e8fbff', 0.9 * a); ctx.stroke()
    for k in range(3):
        ctx.move_to(x - w / 2 + 30 + k * 26, y - h / 2 + 20); ctx.line_to(x - w / 2 + 14 + k * 26, y - h / 2 + 60)
    ctx.set_line_width(6); ctx.set_source_rgba(1, 1, 1, 0.7 * a); ctx.stroke()


def flag_banner(ctx, x, y, txt, col, a=1.0, size=40):
    pill(ctx, x, y, txt, col, C['dark'], size, a)


def elliptic(ctx, x0, y0, sx, sy, a=1.0, col=None, prog_=1.0, lw=8):
    """Draw y^2 = x^3 + 7 (secp256k1 shape) centred at (x0,y0)."""
    if a <= 0 or prog_ <= 0: return
    col = col or C['cyan']
    xs = [-1.913 + i * 0.02 for i in range(0, 300)]
    xr = (7) ** (1 / 3)
    pts_up = []; pts_dn = []
    for xv in xs:
        v = xv ** 3 + 7
        if v < 0: continue
        yv = math.sqrt(v)
        pts_up.append((x0 + xv * sx, y0 - yv * sy)); pts_dn.append((x0 + xv * sx, y0 + yv * sy))
    pts = list(reversed(pts_up)) + pts_dn
    n = max(2, int(len(pts) * prog_))
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:n]: ctx.line_to(*p)
    ctx.set_line_width(lw); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, col, a); ctx.stroke()
