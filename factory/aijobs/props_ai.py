import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solar'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'long'))
from props import *


def bot(ctx, x, y, s=1.0, body='#9aaad6', eye=None, arm_l=0.15, arm_r=0.15, a=1.0, rot=0.0, t=0.0):
    if s <= 1e-3: return
    """Humanoid robot worker, same proportions as person()."""
    eye = eye or C['cyan']
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.25); circle(ctx, 0, 0, 60, C['dark'], 0.35 * a); ctx.restore()
    for lx in (-27, 3):
        rrect(ctx, lx, -72, 24, 72, 8); src(ctx, shade(body, 0.7), a); ctx.fill()
    for side, ang in ((-1, arm_l), (1, arm_r)):
        ctx.save(); ctx.translate(side * 33, -136); ctx.rotate(-side * ang)
        rrect(ctx, -9, -6, 18, 74, 8); src(ctx, shade(body, 0.8), a); ctx.fill()
        circle(ctx, 0, 72, 11, shade(body, 0.9), a); ctx.restore()
    rrect(ctx, -40, -152, 80, 96, 20); src(ctx, body, a); ctx.fill()
    rrect(ctx, -40, -152, 80, 26, 13); ctx.set_source_rgba(1, 1, 1, 0.15 * a); ctx.fill()
    circle(ctx, 0, -104, 12, eye, a)
    rrect(ctx, -34, -222, 68, 62, 20); src(ctx, body, a); ctx.fill()
    rrect(ctx, -26, -208, 52, 26, 12); src(ctx, '#0f1640', a); ctx.fill()
    blink = 0.2 if (t * 0.6 + x * 0.01) % 3.3 < 0.1 else 1.0
    for sx in (-1, 1):
        ctx.save(); ctx.translate(sx * 12, -195); ctx.scale(1, blink); circle(ctx, 0, 0, 6, eye, a); ctx.restore()
    ctx.move_to(0, -222); ctx.line_to(0, -238); ctx.set_line_width(5); src(ctx, shade(body, 0.8), a); ctx.stroke()
    circle(ctx, 0, -240, 6, C['pink'], a)
    ctx.restore()


def truck(ctx, x, y, s, a=1.0, t=0.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -220, -170, 300, 150, 14); src(ctx, '#e8ecff', a); ctx.fill()
    rrect(ctx, 90, -150, 120, 130, 20); src(ctx, C['cyan'], a); ctx.fill()
    rrect(ctx, 130, -132, 64, 50, 10); src(ctx, '#0f1640', a); ctx.fill()
    glow(ctx, 162, -107, 40, C['cyan'], 0.4 * a)
    for wx in (-160, -60, 150):
        circle(ctx, wx, -12, 30, '#232f6e', a); circle(ctx, wx, -12, 12, '#9aaad6', a)
    ctx.restore()


def xray(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -90, 140, 180, 12); src(ctx, '#0f1640', a); ctx.fill()
    ctx.set_line_width(8); src(ctx, '#d4dcf2', a)
    for k in range(5):
        ctx.new_path(); ctx.arc(0, -40 + k * 22, 44, math.pi * 0.15, math.pi * 0.85); ctx.stroke()
    ctx.move_to(0, -70); ctx.line_to(0, 80); ctx.stroke()
    ctx.restore()


def headset(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 50, math.pi, 2 * math.pi); ctx.set_line_width(12); src(ctx, C['white'], a); ctx.stroke()
    for sx in (-1, 1): rrect(ctx, sx * 50 - 14, -10, 28, 44, 10); src(ctx, C['white'], a); ctx.fill()
    ctx.move_to(50, 30); ctx.curve_to(50, 60, 20, 70, 0, 66); ctx.set_line_width(7); ctx.stroke()
    circle(ctx, 0, 66, 9, C['pink'], a)
    ctx.restore()


def gavel(ctx, x, y, s, ang=0.0, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(ang)
    rrect(ctx, -10, -150, 20, 150, 10); src(ctx, '#8c6a45', a); ctx.fill()
    rrect(ctx, -60, -200, 120, 60, 18); src(ctx, '#b0875a', a); ctx.fill(); ctx.restore()


def alarm_clock(ctx, x, y, s, t, ring=0.0, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.08 * math.sin(t * 40) * ring)
    for sx in (-1, 1): circle(ctx, sx * 38, -52, 20, C['yellow'], a)
    circle(ctx, 0, 0, 60, C['red'], a); circle(ctx, 0, 0, 46, C['white'], a)
    ctx.move_to(0, 0); ctx.line_to(0, -32); ctx.move_to(0, 0); ctx.line_to(22, 8); ctx.set_line_width(6)
    src(ctx, C['dark'], a); ctx.stroke(); ctx.restore()


def loom(ctx, x, y, s, t, broken=0.0, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, '#8c6a45', a)
    ctx.move_to(-160, 0); ctx.line_to(-160, -260); ctx.move_to(160, 0); ctx.line_to(160 + 60 * broken, -260 + 80 * broken)
    ctx.move_to(-160, -240); ctx.line_to(160, -240 + 120 * broken); ctx.move_to(-160, -60); ctx.line_to(160, -60); ctx.stroke()
    for k in range(14):
        xx = -140 + k * 20
        ctx.move_to(xx, -230 + 8 * broken * k); ctx.line_to(xx, -70); ctx.set_line_width(3); src(ctx, '#ffd28a', a * (1 - 0.6 * broken))
        ctx.stroke()
    rrect(ctx, -150, -170 + 20 * math.sin(t * 4) * (1 - broken), 300, 30, 10); src(ctx, '#b0875a', a); ctx.fill()
    ctx.restore()


def atm(ctx, x, y, s, a=1.0, t=0.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -90, -300, 180, 300, 18); src(ctx, '#5a6ab8', a); ctx.fill()
    rrect(ctx, -60, -260, 120, 80, 10); src(ctx, C['cyan'], a); ctx.fill()
    rich(ctx, [('ATM', C['dark'])], 0, -220, 34, a, pop=False, shadow=False)
    for k in range(9):
        rrect(ctx, -50 + (k % 3) * 36, -160 + (k // 3) * 30, 28, 22, 5); src(ctx, '#d4dcf2', a); ctx.fill()
    rrect(ctx, -50, -60, 100, 14, 6); src(ctx, '#0f1640', a); ctx.fill()
    ctx.restore()


def bank(ctx, x, y, s, a=1.0, col='#d4dcf2'):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-130, -170); ctx.line_to(0, -240); ctx.line_to(130, -170); ctx.close_path(); src(ctx, col, a); ctx.fill()
    rrect(ctx, -130, -170, 260, 20, 4); ctx.fill()
    for k in range(4): rrect(ctx, -105 + k * 64, -145, 30, 125, 6); src(ctx, col, a); ctx.fill()
    rrect(ctx, -140, -24, 280, 24, 4); src(ctx, col, a); ctx.fill()
    rich(ctx, [('$', C['dark'])], 0, -196, 38, a, pop=False, shadow=False)
    ctx.restore()


def brain(ctx, x, y, s, col=None, a=1.0, t=0.0):
    if s <= 1e-3: return
    col = col or C['pink']
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for (bx, by, br) in ((-40, -20, 52), (10, -40, 56), (50, -5, 48), (-20, 30, 50), (35, 35, 44)):
        circle(ctx, bx, by, br, col, a)
    ctx.set_line_width(7); ctx.set_source_rgba(1, 1, 1, 0.35 * a)
    for (cx_, cy_) in ((-30, -10), (20, -30), (30, 25)):
        ctx.new_path(); ctx.arc(cx_, cy_, 22, 0.3, 2.6); ctx.stroke()
    ctx.move_to(5, -90); ctx.line_to(5, 75); ctx.set_source_rgba(0, 0, 0.2, 0.2 * a); ctx.stroke()
    ctx.restore()


def muscle(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-90, 60); ctx.line_to(-30, 60); ctx.curve_to(10, 60, 20, 20, 10, -10); ctx.curve_to(0, -40, 20, -80, 50, -70)
    ctx.curve_to(80, -60, 70, -20, 50, -10); ctx.curve_to(70, 10, 80, 60, 30, 90); ctx.line_to(-90, 90); ctx.close_path()
    src(ctx, C['skin'], a); ctx.fill(); ctx.restore()


def calc(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -45, -60, 90, 120, 12); src(ctx, C['white'], a); ctx.fill()
    rrect(ctx, -35, -50, 70, 28, 6); src(ctx, '#20307e', a); ctx.fill()
    for k in range(9):
        rrect(ctx, -33 + (k % 3) * 24, -12 + (k // 3) * 22, 18, 16, 4); src(ctx, '#9aaad6', a); ctx.fill()
    ctx.restore()


def pen(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(0.7)
    rrect(ctx, -12, -70, 24, 110, 8); src(ctx, C['white'], a); ctx.fill()
    ctx.move_to(-12, 40); ctx.line_to(0, 70); ctx.line_to(12, 40); ctx.close_path(); src(ctx, C['yellow'], a); ctx.fill()
    ctx.restore()


def box(ctx, x, y, s, col='#d9a066', a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -30, -50, 60, 50, 6); src(ctx, col, a); ctx.fill()
    ctx.rectangle(-6, -50, 12, 50); src(ctx, shade(col, 0.8), a); ctx.fill(); ctx.restore()


def envelope(ctx, x, y, s, a=1.0, col=None):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -50, -32, 100, 64, 8); src(ctx, col or C['white'], a); ctx.fill()
    ctx.move_to(-50, -30); ctx.line_to(0, 6); ctx.line_to(50, -30); ctx.set_line_width(5); src(ctx, '#9aaad6', a); ctx.stroke()
    rich(ctx, [('$', C['green'])], 0, 14, 30, a, pop=False, shadow=False)
    ctx.restore()


def derrick(ctx, x, y, s, a=1.0, t=0.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.set_line_width(8); ctx.set_line_join(cairo.LINE_JOIN_ROUND); src(ctx, '#2a2f5a', a)
    ctx.move_to(-70, 0); ctx.line_to(0, -280); ctx.line_to(70, 0)
    for k in range(5):
        yy = -50 - k * 50; w = 70 * (1 + yy / 280)
        ctx.move_to(-w, yy); ctx.line_to(w, yy)
    ctx.stroke(); ctx.restore()


def server(ctx, x, y, s, a=1.0, t=0.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -70, -280, 140, 280, 12); src(ctx, '#20307e', a); ctx.fill()
    for k in range(7):
        rrect(ctx, -56, -265 + k * 38, 112, 28, 6); src(ctx, '#2f4aa8', a); ctx.fill()
        on = math.sin(t * 7 + k * 1.7) > 0
        circle(ctx, 40, -251 + k * 38, 5, C['green'] if on else C['cyan'], a)
    ctx.restore()


def chessboard(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i in range(8):
        for j in range(8):
            ctx.rectangle(-160 + i * 40, -160 + j * 40, 40, 40); src(ctx, '#e8d4b0' if (i + j) % 2 == 0 else '#8c6a45', a); ctx.fill()
    for (i, j, col) in ((3, 6, '#ffffff'), (4, 7, '#ffffff'), (2, 1, '#151032'), (5, 0, '#151032'), (4, 3, '#ffffff')):
        cx_, cy_ = -140 + i * 40, -140 + j * 40
        circle(ctx, cx_, cy_ - 8, 10, col, a); rrect(ctx, cx_ - 12, cy_ - 2, 24, 14, 5); src(ctx, col, a); ctx.fill()
    ctx.restore()


def monitor(ctx, x, y, s, a=1.0, screen=None):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rrect(ctx, -110, -170, 220, 150, 12); src(ctx, '#d4dcf2', a); ctx.fill()
    rrect(ctx, -98, -158, 196, 126, 8); src(ctx, screen or '#0f1640', a); ctx.fill()
    rrect(ctx, -15, -20, 30, 20, 4); src(ctx, '#9aaad6', a); ctx.fill(); rrect(ctx, -50, 0, 100, 10, 5); ctx.fill()
    ctx.restore()


def top_hat_owner(ctx, x, y, s, a=1.0):
    if s <= 1e-3: return
    person(ctx, x, y, s, shirt='#2a2f5a', arm_l=0.3, arm_r=1.4, a=a)
    rrect(ctx, x - 30 * s, y - 230 * s - 60 * s, 60 * s, 60 * s, 6); src(ctx, '#151032', a); ctx.fill()
    rrect(ctx, x - 48 * s, y - 230 * s - 4 * s, 96 * s, 10 * s, 5); ctx.fill()


def heart(ctx, x, y, s, col=None, a=1.0):
    if s <= 1e-3: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, 30); ctx.curve_to(-60, -10, -40, -60, 0, -30); ctx.curve_to(40, -60, 60, -10, 0, 30)
    src(ctx, col or C['pink'], a); ctx.fill(); ctx.restore()
