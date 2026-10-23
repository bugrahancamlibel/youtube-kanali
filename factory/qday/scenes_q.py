from props_q import *


def starts(L): return [a for a, b in L]


def fade_block(ctx, a, fn):
    if a <= 0: return
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def win(lt, a0, a1, f=0.25):
    return prog(lt, a0 - f, a0 + f) * (1 - prog(lt, a1 - f, a1 + f))


def label(ctx, txt, x, y, size, col, p, w='bold', maxw=900):
    rich(ctx, [(txt, col)], x, y, size, p, maxw=maxw, w=w)


def morning_bg(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#3a5ad8')); g.add_color_stop_rgba(1, *hexc('#f0a07a'))
    ctx.set_source(g); ctx.paint()
    glow(ctx, 1500, 300, 600, '#ffd23f', 0.45)
    circle(ctx, 1500, 300, 90, '#fff3c0')
    hills(ctx, 900, '#5a4aa8', amp=30, phase=0.5)
    hills(ctx, 960, '#3a2f7e', amp=20, phase=2.0)


def night_bg(ctx, t, glow_col='#4a2a9a'):
    bg(ctx, t, top='#050a24', bot='#141f5a', glow_col=glow_col, gy=700)


# ===================================================================== 0  COLD OPEN
def s0(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def morning():
        morning_bg(ctx, t)
        person(ctx, 520, 930, 2.3, shirt=C['orange'], arm_l=0.2, arm_r=0.9)
        phone(ctx, 640, 640, 0.45, screen=C['cyan'])
        items = [(l0 + 1.6, 'tap your card', card_icon, C['pink']), (l0 + 3.0, 'send a message', None, C['cyan']),
                 (l0 + 4.3, 'log into your bank', None, C['green'])]
        for k, (st, lab, fn, col) in enumerate(items):
            p = prog(lt, st, st + 0.45)
            if p <= 0: continue
            cx, cy = 1040 + k * 250, 420 + (k % 2) * 90
            def ic(cx=cx, cy=cy, k=k, col=col):
                card(ctx, cx - 105, cy - 105, 210, 210, '#20307e', 40)
                if k == 0: card_icon(ctx, cx, cy - 10, 1.9, col)
                elif k == 1:
                    bubble(ctx, cx, cy - 20, 'Hi!', col, 1.0)
                else: bank(ctx, cx, cy + 70, 0.55)
                padlock(ctx, cx + 80, cy + 80, 0.42, body=C['green'])
            pop_scale(ctx, cx, cy, p, ic)
            label(ctx, lab, cx, cy + 160, 34, C['white'], p, maxw=240)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), morning)

    def supercomp():
        night_bg(ctx, t, glow_col='#3a2a8a')
        hills(ctx, 900, '#0d1540', amp=0)
        for k in range(6):
            server(ctx, 220 + k * 120, 880, 1.0, t=t + k)
        glow(ctx, 520, 760, 420, C['orange'], 0.25 + 0.1 * math.sin(t * 5))
        label(ctx, 'SUPERCOMPUTERS', 520, 940, 34, C['grey'], prog(lt, l1 + 0.6, l1 + 1.0))
        pl = eback(prog(lt, l1 + 0.2, l1 + 0.7))
        padlock(ctx, 1320, 500, 2.2 * pl, body=C['yellow'])
        for k in range(10):
            ph = (t * 0.6 + k / 10) % 1
            ang = k * 0.63
            x = 1320 + math.cos(ang) * (420 - 300 * ph); y = 470 + math.sin(ang) * (300 - 200 * ph)
            rich(ctx, [(random.Random(k).choice(['x^3', 'mod N', 'p·q', '2^256', 'ECC', 'RSA']), C['cyan'])], x, y, 30,
                 (1 - ph) * prog(lt, l1 + 0.5, l1 + 1.0), pop=False, shadow=False)
        # crawling progress
        pb = prog(lt, l1 + 1.5, l1 + 2.0)
        if pb > 0:
            rrect(ctx, 1020, 760, 600, 36, 18); src(ctx, '#1d2c6e', pb); ctx.fill()
            rrect(ctx, 1020, 760, 8 + 6 * prog(lt, l1 + 2, l1 + 8), 36, 18); src(ctx, C['pink'], pb); ctx.fill()
            label(ctx, 'cracking... 0.0000001%', 1320, 830, 30, C['grey'], pb, w='normal')
        hg = prog(lt, l1 + 5.0, l1 + 5.5)
        hourglass(ctx, 1700, 450, 0.9 * eback(hg), t)
        pill(ctx, 1320, 130, 'MILLIONS OF YEARS', C['yellow'], C['dark'], 46, hg)
    fade_block(ctx, win(lt, l1 - 0.2, l2), supercomp)

    def quantum():
        night_bg(ctx, t, glow_col='#5a2aa8')
        d = eo(prog(lt, l2 + 0.2, l2 + 1.4))
        qcomputer(ctx, 1320, -560 + 600 * d, 1.0, t, glow_a=0.6 + 0.4 * prog(lt, l2 + 1.6, l2 + 2.4))
        beam = prog(lt, l2 + 1.6, l2 + 2.2) * (1 - prog(lt, l2 + 3.6, l2 + 4.2))
        if beam > 0:
            ctx.move_to(1320, 600); ctx.line_to(640, 520); ctx.set_line_width(24 * beam); src(ctx, Q, 0.5 * beam); ctx.stroke()
            ctx.move_to(1320, 600); ctx.line_to(640, 520); ctx.set_line_width(8 * beam); src(ctx, '#f0e6ff', beam); ctx.stroke()
        op = prog(lt, l2 + 2.6, l2 + 3.2)
        padlock(ctx, 640, 520, 2.2, open_=op, body=lerp_col(C['yellow'], C['red'], op) if op > 0 else C['yellow'])
        if op > 0.3:
            for k in range(12):
                ph = clamp((lt - l2 - 2.8) / 1.2)
                ang = k * 0.52
                circle(ctx, 640 + math.cos(ang) * 260 * ph, 520 + math.sin(ang) * 220 * ph, 9 * (1 - ph), C['yellow'], 1 - ph)
        pill(ctx, 640, 860, 'BROKEN IN DAYS', C['pink'], C['white'], 46, prog(lt, l2 + 3.2, l2 + 3.6))
    fade_block(ctx, win(lt, l2 - 0.2, l3), quantum)

    def city_open():
        night_bg(ctx, t, glow_col='#2a2a7a')
        city(ctx, 900, t, 0.8, seed=31)
        hills(ctx, 940, '#0a1035', amp=0)
        spots = [(330, 360), (620, 300), (900, 380), (1180, 290), (1460, 360), (1650, 260), (480, 210), (1320, 180)]
        for k, (x, y) in enumerate(spots):
            st = l3 + 1.6 + k * 0.32
            op = prog(lt, st, st + 0.4)
            padlock(ctx, x, y, 0.55, open_=op, body=C['yellow'] if op < 0.5 else C['pink'])
            if op > 0.6:
                for j in range(3):
                    rrect(ctx, x - 50, y + 70 + j * 22, 100 - j * 20, 10, 5); src(ctx, C['white'], 0.7 * prog(lt, st + 0.4, st + 0.8)); ctx.fill()
        label(ctx, 'no alarms  ·  no explosions', 960, 110, 44, C['grey'], prog(lt, l3 + 0.2, l3 + 0.6) * (1 - prog(lt, l3 + 4.0, l3 + 4.4)), w='normal')
        stamp(ctx, 960, 560, 'Q-DAY', C['pink'], prog(lt, l3 + 4.6, l3 + 5.0), size=170)
    te = L[3][1]
    fade_block(ctx, win(lt, l3 - 0.2, te + 0.3), city_open)

    def ttl():
        night_bg(ctx, t, glow_col='#5a2aa8')
        qcomputer(ctx, 1690, -70, 0.55, t)
        padlock(ctx, 250, 850, 1.2, open_=1.0, body=C['pink'])
        rich(ctx, [('WHAT IF', C['white'])], 960, 270, 90, prog(lt, te + 0.2, te + 0.5))
        rich(ctx, [('QUANTUM COMPUTERS', Q)], 960, 420, 120, prog(lt, te + 0.35, te + 0.65), maxw=1300)
        rich(ctx, [('BROKE ALL ', C['white']), ('ENCRYPTION?', C['yellow'])], 960, 580, 110, prog(lt, te + 0.5, te + 0.8), maxw=1300)
    fade_block(ctx, prog(lt, te + 0.1, te + 0.5), ttl)


# ===================================================================== 1  THE PADLOCK
FRIENDS = [(1250, C['cyan']), (1500, C['green']), (1750, C['pink'])]


def s1(ctx, lt, t, L):
    l0, l1 = starts(L)
    bg(ctx, t, glow_col='#2a4a9a', gy=600)
    hills(ctx, 900, '#1a2766', amp=0)

    def give():
        person(ctx, 360, 900, 1.8, shirt=C['orange'], arm_l=0.4, arm_r=0.9)
        label(ctx, 'YOU', 360, 960, 36, C['orange'], 1.0)
        for k, (fx, col) in enumerate(FRIENDS):
            person(ctx, fx, 900, 1.5, shirt=col, arm_l=0.3, arm_r=0.6)
            st = l0 + 1.8 + k * 0.6
            p = ss(prog(lt, st, st + 0.9))
            if p < 1:
                x = lerp(470, fx - 40, p); y = 560 - 260 * math.sin(math.pi * p)
                padlock(ctx, x, y, 0.5, open_=1.0)
            else:
                shut = prog(lt, l0 + 5.0 + k * 0.3, l0 + 5.4 + k * 0.3)
                if k != 1:
                    padlock(ctx, fx + 70, 640, 0.5, open_=1 - shut)
        # middle friend locks a box and sends it back
        bp = prog(lt, l0 + 4.6, l0 + 5.0)
        if bp > 0:
            back = ss(prog(lt, l0 + 6.2, l0 + 7.4))
            bx = lerp(1500 + 90, 520, back); by = 640 - 200 * math.sin(math.pi * back)
            rrect(ctx, bx - 70, by - 40, 140, 100, 12); src(ctx, '#d9a066', bp); ctx.fill()
            envelope(ctx, bx, by + 10, 0.45, a=bp * (1 - prog(lt, l0 + 5.4, l0 + 5.6)))
            shut = prog(lt, l0 + 5.4, l0 + 5.9)
            padlock(ctx, bx, by - 40, 0.45, open_=1 - shut)
        pill(ctx, 960, 170, 'PUBLIC KEY = an open padlock', C['yellow'], C['dark'], 44, prog(lt, l0 + 0.6, l0 + 1.0))
        rich(ctx, [('anyone can snap it shut', C['grey'])], 960, 250, 36, prog(lt, l0 + 5.0, l0 + 5.4), w='normal')
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), give)

    def private():
        person(ctx, 330, 900, 1.8, shirt=C['orange'], arm_l=0.4, arm_r=1.3)
        kp = eback(prog(lt, l1 + 0.3, l1 + 0.8))
        key(ctx, 460, 620, 1.2 * kp, rot=-0.3)
        op = prog(lt, l1 + 1.4, l1 + 2.0)
        rrect(ctx, 500, 660, 160, 110, 14); src(ctx, '#d9a066'); ctx.fill()
        padlock(ctx, 580, 640, 0.6, open_=op)
        pill(ctx, 430, 170, 'PRIVATE KEY: only you', GOLD, C['dark'], 40, prog(lt, l1 + 0.6, l1 + 1.0))
        # the hard way back
        pc = prog(lt, l1 + 3.0, l1 + 3.5)
        if pc > 0:
            card(ctx, 900, 300, 900, 520, '#162263', 40)
            rich(ctx, [('13 x 17 = 221', C['green'])], 1350, 400, 70, pc, pop=False)
            rich(ctx, [('easy', C['green'])], 1350, 470, 34, pc, w='normal', pop=False)
            p2 = prog(lt, l1 + 4.3, l1 + 4.8)
            rich(ctx, [('221 = ? x ?', C['pink'])], 1350, 590, 70, p2, pop=False)
            p3 = prog(lt, l1 + 5.6, l1 + 6.1)
            if p3 > 0:
                rnd = random.Random(int(t * 6))
                digits = ''.join(str(rnd.randint(0, 9)) for _ in range(46))
                rich(ctx, [(digits, C['grey'])], 1350, 690, 30, p3, pop=False, w='normal', maxw=820)
                rich(ctx, [('a real key: 617 digits long', C['yellow'])], 1350, 760, 36, p3, pop=False)
        ap = prog(lt, l1 + 2.2, l1 + 2.8)
        if ap > 0:
            ctx.move_to(780, 470); ctx.curve_to(700, 360, 600, 360, 540, 440)
            ctx.set_line_width(10); ctx.set_dash([18, 14]); src(ctx, C['grey'], ap); ctx.stroke(); ctx.set_dash([])
            x_mark(ctx, 680, 380, 40, prog(lt, l1 + 6.8, l1 + 7.4))
            rich(ctx, [('padlock  to  key?', C['white'])], 680, 290, 34, ap, pop=False, w='normal')
    fade_block(ctx, prog(lt, l1 - 0.2, l1 + 0.3), private)


# ===================================================================== 2  QUANTUM COMPUTERS
def s2(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#0a0f33', bot='#26165e', glow_col='#5a2aa8', gy=560)

    def qubits():
        pa = prog(lt, l0 + 0.4, l0 + 0.8)
        v = 1.0 if (t * 1.3) % 2 < 1 else 0.0
        pop_scale(ctx, 480, 420, pa, lambda: bit_switch(ctx, 480, 420, 1.3, v))
        label(ctx, 'BIT', 480, 640, 52, C['grey'], pa)
        rich(ctx, [('0 or 1', C['white'])], 480, 700, 34, pa, w='normal')
        pb = prog(lt, l0 + 1.6, l0 + 2.2)
        bloch(ctx, 1380, 420, 170 * eback(pb), t, a=pb)
        label(ctx, 'QUBIT', 1380, 680, 52, Q, pb)
        rich(ctx, [('superposition', C['white'])], 1380, 740, 34, pb, w='normal')
        # interference waves
        pw = prog(lt, l0 + 4.4, l0 + 5.0)
        if pw > 0:
            for k, (col, ph) in enumerate(((C['cyan'], 0), (C['pink'], 0.0))):
                ctx.new_path()
                for x in range(560, 1360, 8):
                    y = 860 + (k * 2 - 1) * 0 + 34 * math.sin(x / 40 - t * 5 + ph) * (1 - prog(lt, l0 + 5.6, l0 + 6.4) * (x > 960))
                    ctx.line_to(x, y - 40 + 80 * k if x < 960 else y)
                ctx.set_line_width(6); src(ctx, col, pw); ctx.stroke()
            big = prog(lt, l0 + 5.6, l0 + 6.4)
            ctx.new_path()
            for x in range(960, 1360, 8):
                ctx.line_to(x, 860 + 64 * big * math.sin(x / 40 - t * 5))
            ctx.set_line_width(10); src(ctx, C['yellow'], pw * big); ctx.stroke()
            rich(ctx, [('interference', C['yellow'])], 1500, 860, 34, pw * big, w='normal', pop=False)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), qubits)

    def shor():
        rrect(ctx, 260, 160, 1000, 600, 24); src(ctx, '#1f3d36'); ctx.fill()
        rrect(ctx, 260, 160, 1000, 600, 24); ctx.set_line_width(18); src(ctx, '#8c6a45'); ctx.stroke()
        pw = prog(lt, l1 + 0.3, l1 + 0.8)
        rich(ctx, [('1994', C['yellow'])], 760, 280, 110, pw, pop=False, shadow=False)
        rich(ctx, [("Shor's algorithm", C['white'])], 760, 420, 70, prog(lt, l1 + 1.6, l1 + 2.1), pop=False, shadow=False)
        rich(ctx, [('N  ->  p x q', '#bfe8d8')], 760, 540, 56, prog(lt, l1 + 2.4, l1 + 2.9), pop=False, shadow=False, w='normal')
        rich(ctx, [('in polynomial time', '#bfe8d8')], 760, 630, 40, prog(lt, l1 + 2.8, l1 + 3.3), pop=False, shadow=False, w='normal')
        person(ctx, 1460, 900, 1.9, shirt='#5a6ab8', arm_l=0.2, arm_r=2.0)
        rich(ctx, [('Peter Shor', C['grey'])], 1460, 960, 32, pw, w='normal')
        lp = prog(lt, l1 + 4.2, l1 + 4.7)
        if lp > 0:
            padlock(ctx, 1700, 360, 1.0 * eback(lp), open_=prog(lt, l1 + 5.2, l1 + 5.8))
            key(ctx, 1600, 520, 0.9 * eback(lp), rot=-0.5, col=Q)
            glow(ctx, 1600, 520, 140, Q, 0.5 * lp)
    fade_block(ctx, win(lt, l1 - 0.2, l2), shor)

    def noisy():
        rnd = random.Random(int(t * 12))
        jit = 6
        chip_grid(ctx, 960 + rnd.uniform(-jit, jit), 470 + rnd.uniform(-jit, jit), 300, 3, t, col=C['red'] if rnd.random() < 0.4 else C['cyan'])
        label(ctx, 'only theory', 960, 160, 60, C['grey'], prog(lt, l2 + 0.2, l2 + 0.6), w='normal')
        for k, (txt, x, y) in enumerate((('ERROR', 620, 330), ('NOISE', 1320, 380), ('ERROR', 700, 640), ('TOO SMALL', 1290, 650))):
            st = l2 + 1.6 + k * 0.6
            pill(ctx, x, y, txt, C['red'], C['white'], 36, prog(lt, st, st + 0.3) * (0.7 + 0.3 * math.sin(t * 9 + k)))
    fade_block(ctx, win(lt, l2 - 0.2, l3), noisy)

    def willow():
        z = ss(prog(lt, l3 + 3.4, l3 + 5.6))
        sc = lerp(1.0, 0.16, z)
        ctx.save(); ctx.translate(960, 460); ctx.scale(sc, sc); ctx.translate(-960, -460)
        if z > 0:
            for i in range(-9, 10):
                for j in range(-5, 6):
                    if i == 0 and j == 0: continue
                    d = abs(i) + abs(j)
                    pa = prog(lt, l3 + 3.6 + d * 0.08, l3 + 4.0 + d * 0.08)
                    chip_grid(ctx, 960 + i * 420, 460 + j * 420, 380, 6, t + i + j, a=pa * 0.85, col='#6b7fb8')
        chip_grid(ctx, 960, 460, 380, 10, t)
        ctx.restore()
        pa = prog(lt, l3 + 0.4, l3 + 0.8) * (1 - z)
        label(ctx, "Google's Willow chip (2024)", 960, 140, 54, C['white'], pa)
        pill(ctx, 960, 760, '105 QUBITS', C['cyan'], C['dark'], 50, prog(lt, l3 + 1.4, l3 + 1.8) * (1 - z))
        pz = prog(lt, l3 + 5.0, l3 + 5.5)
        if pz > 0:
            rrect(ctx, 460, 70, 1000, 130, 30); src(ctx, '#05081a', 0.75 * pz); ctx.fill()
            label(ctx, 'needed to break encryption: far bigger', 960, 135, 50, C['yellow'], pz, maxw=920)
            circle(ctx, 960, 460, 34, C['cyan'], 0.9 * pz)
            rich(ctx, [('Willow', C['cyan'])], 960, 530, 30, pz, pop=False)
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), willow)


# ===================================================================== 3  THE SHRINKING TARGET
BARS = [('2012', 1e9, 'up to 1 billion', C['pink']), ('2019', 2e7, '20 million', C['orange']),
        ('2025', 1e6, 'under 1 million', C['yellow']), ('2026', 1e5, 'under 100,000', C['cyan'])]


def bar_h(v): return (math.log10(v) - 1) / 8 * 520


def s3(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#0b1640', bot='#22195e', glow_col='#3a2a8a', gy=600)

    def shrink():
        z = ss(prog(lt, l0 + 1.2, l0 + 4.0))
        sz = lerp(820, 260, z)
        chip_grid(ctx, 960, 520, sz, 12, t, col='#ff8aa8')
        label(ctx, 'the machine needed keeps shrinking', 960, 110, 50, C['white'], prog(lt, l0 + 0.4, l0 + 0.8) * (1 - prog(lt, l1 - 0.6, l1 - 0.2)))
    fade_block(ctx, 1 - prog(lt, l1 - 0.3, l1 + 0.2), shrink)

    base = 860
    def chart():
        label(ctx, 'QUBITS NEEDED TO BREAK RSA ENCRYPTION', 960, 90, 46, C['white'], prog(lt, l1 - 0.1, l1 + 0.3), maxw=1500)
        ctx.move_to(220, base); ctx.line_to(1720, base); ctx.set_line_width(4); ctx.set_source_rgba(1, 1, 1, 0.4); ctx.stroke()
        rich(ctx, [('log scale', C['grey'])], 1700, base + 40, 24, prog(lt, l1, l1 + 0.4), w='normal', pop=False)
        starts_ = [l1 + 0.6, l1 + 7.0, l1 + 8.6, l2 + 1.0]
        for k, ((yr, v, lab, col), st) in enumerate(zip(BARS, starts_)):
            g = eo(prog(lt, st, st + 1.4))
            if g <= 0: continue
            x = 330 + k * 300
            hh = bar_h(v) * g
            rrect(ctx, x - 90, base - hh, 180, hh, 16); src(ctx, col); ctx.fill()
            rich(ctx, [(yr, C['white'])], x, base + 40, 36, g, pop=False)
            rich(ctx, [(lab, col)], x, base - hh - 40, 34, prog(lt, st + 0.8, st + 1.2), maxw=280)
        # dashed claim
        st = l2 + 3.2
        g = eo(prog(lt, st, st + 1.2))
        if g > 0:
            x = 1530; hh = bar_h(1e4) * g
            rrect(ctx, x - 90, base - hh, 180, hh, 16); ctx.set_dash([14, 10]); ctx.set_line_width(5); src(ctx, C['green']); ctx.stroke(); ctx.set_dash([])
            rich(ctx, [('2026 claim', C['white'])], x, base + 40, 32, g, pop=False)
            rich(ctx, [('~10,000?', C['green'])], x, base - hh - 40, 36, prog(lt, st + 0.6, st + 1.0))
            rich(ctx, [('(by researchers at a quantum startup)', C['grey'])], x - 100, base + 82, 24, prog(lt, st + 0.8, st + 1.2), w='normal', pop=False)
        # willow line
        wl = prog(lt, l1 + 2.0, l1 + 2.6)
        if wl > 0:
            yy = base - bar_h(105)
            ctx.move_to(220, yy); ctx.line_to(220 + 1500 * wl, yy); ctx.set_dash([10, 10]); ctx.set_line_width(4); src(ctx, C['cyan'], 0.8); ctx.stroke(); ctx.set_dash([])
            ctx.move_to(1330, 190); ctx.line_to(1400, 190); ctx.set_dash([10, 8]); ctx.set_line_width(5); src(ctx, C['cyan'], wl); ctx.stroke(); ctx.set_dash([])
            rich(ctx, [("today's best chips: ~100 qubits", C['cyan'])], 1420, 190, 28, wl, w='normal', pop=False, align='left', maxw=420)
        # counter for the 2012 bar
        cnt = prog(lt, l1 + 0.6, l1 + 6.0)
        if 0 < cnt < 1:
            rich(ctx, [(counter_text(10 ** (1 + 8 * eo(cnt))), C['pink'])], 330, 220, 44, 1.0, pop=False)
    fade_block(ctx, win(lt, l1 - 0.2, l3), chart)

    def converge():
        label(ctx, 'THE GAP IS CLOSING', 960, 110, 64, C['white'], prog(lt, l3 + 0.1, l3 + 0.5))
        ctx.move_to(240, 880); ctx.line_to(1700, 880); ctx.move_to(240, 880); ctx.line_to(240, 230)
        ctx.set_line_width(4); ctx.set_source_rgba(1, 1, 1, 0.4); ctx.stroke()
        p = prog(lt, l3 + 0.4, l3 + 3.2)
        n = int(60 * p)
        ctx.new_path()
        for i in range(n + 1):
            u = i / 60
            ctx.line_to(240 + 1300 * u, 280 + 420 * (1 - (1 - u) ** 1.8))
        ctx.set_line_width(10); src(ctx, C['pink']); ctx.stroke()
        ctx.new_path()
        for i in range(n + 1):
            u = i / 60
            ctx.line_to(240 + 1300 * u, 860 - 160 * u ** 2.2 - 260 * u ** 6)
        ctx.set_line_width(10); src(ctx, C['green']); ctx.stroke()
        rich(ctx, [('qubits needed', C['pink'])], 420, 250, 36, prog(lt, l3 + 0.6, l3 + 1.0), pop=False)
        rich(ctx, [('qubits built', C['green'])], 470, 900 - 80, 36, prog(lt, l3 + 0.6, l3 + 1.0), pop=False)
        qd = prog(lt, l3 + 3.0, l3 + 3.4)
        if qd > 0:
            glow(ctx, 1302, 680, 200, C['yellow'], 0.6 * qd)
            circle(ctx, 1302, 680, 16 * eback(qd), C['yellow'])
            pill(ctx, 1302, 580, 'Q-DAY?', C['yellow'], C['dark'], 46, qd)
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), converge)


# ===================================================================== 4  Q-DAY
def s4(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    night_bg(ctx, t, glow_col='#6a1a3a')

    def cal():
        flip = prog(lt, l0 + 0.6, l0 + 1.2)
        calendar(ctx, 960, 500, 2.0, 'TOMORROW', 'Q-DAY' if flip > 0.5 else '?', col=C['red'], big_col=C['red'])
        glow(ctx, 960, 500, 700, C['red'], 0.25 * (0.5 + 0.5 * math.sin(t * 6)) * flip)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), cal)

    def opened():
        items = [('bank connections', 'bank'), ('card payments', 'card'), ('private messages', 'msg')]
        for k, (lab, kind) in enumerate(items):
            cx = 420 + k * 540; cy = 470
            pa = prog(lt, l1 + 0.2 + k * 0.25, l1 + 0.6 + k * 0.25)
            def body(cx=cx, cy=cy, kind=kind):
                card(ctx, cx - 210, cy - 230, 420, 460, '#1b2766', 44)
                if kind == 'bank': bank(ctx, cx, cy + 110, 0.9)
                elif kind == 'card': card_icon(ctx, cx, cy - 20, 3.6, C['pink'])
                else:
                    bubble(ctx, cx - 30, cy - 60, 'see you at 8', C['cyan'], 1.0)
                    bubble(ctx, cx + 40, cy + 50, 'PIN: 4471', C['green'], 1.0)
            pop_scale(ctx, cx, cy, pa, body)
            op = prog(lt, l1 + 1.6 + k * 1.2, l1 + 2.1 + k * 1.2)
            padlock(ctx, cx + 150, cy - 190, 0.8 * eback(pa), open_=op, body=C['green'] if op < 0.5 else C['red'])
            if op > 0: glow(ctx, cx, cy, 300, C['red'], 0.3 * op * (1 - prog(lt, l1 + 2.4 + k * 1.2, l1 + 3.2 + k * 1.2)))
            label(ctx, lab, cx, cy + 290, 38, C['white'], pa)
        label(ctx, 'every old lock opens', 960, 100, 54, C['pink'], prog(lt, l1 + 0.4, l1 + 0.8))
    fade_block(ctx, win(lt, l1 - 0.2, l2), opened)

    def forged():
        def page():
            rich(ctx, [('Your Bank', '#20307e')], 560, 330, 64, 1.0, pop=False, shadow=False)
            for j in range(2):
                rrect(ctx, 340, 400 + j * 90, 440, 60, 14); src(ctx, '#d4dcf2'); ctx.fill()
            rrect(ctx, 340, 590, 440, 64, 32); src(ctx, '#2d6be0'); ctx.fill()
            rich(ctx, [('Log in', C['white'])], 560, 622, 34, 1.0, pop=False, shadow=False)
        pa = prog(lt, l2 + 0.2, l2 + 0.6)
        if pa > 0:
            ctx.push_group()
            browser(ctx, 240, 200, 640, 520, 'yourbank.com', lock=True, body=page)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(pa)
        hooded(ctx, 950, 900, 1.6, a=prog(lt, l2 + 1.4, l2 + 1.8), t=t, arm_r=0.9)
        pill(ctx, 560, 800, 'FAKE, but looks real', C['red'], C['white'], 36, prog(lt, l2 + 1.8, l2 + 2.2))
        pp = prog(lt, l2 + 2.6, l2 + 3.0)
        if pp > 0:
            phone(ctx, 1450, 480, 1.25, screen='#1b2a6e')
            def upd(c):
                rrect(c, 1360, 380, 180, 210, 16); src(c, C['white']); c.fill()
                rich(c, [('UPDATE', C['dark'])], 1450, 430, 34, 1.0, pop=False, shadow=False)
                rich(c, [('verified', C['green'])], 1450, 480, 28, 1.0, pop=False, shadow=False, w='normal')
                rrect(c, 1385, 520, 130, 46, 23); src(c, C['green']); c.fill()
                rich(c, [('Install', C['white'])], 1450, 544, 26, 1.0, pop=False, shadow=False)
            gl = 0.5 * prog(lt, l2 + 3.4, l2 + 3.8) * (math.sin(t * 13) > 0.3)
            glitched(ctx, upd, 1340, 360, 230, 240, gl, int(t * 10))
            pill(ctx, 1450, 800, 'FORGED UPDATE', C['red'], C['white'], 36, prog(lt, l2 + 3.6, l2 + 4.0))
    fade_block(ctx, win(lt, l2 - 0.2, l3), forged)

    def harvest():
        hooded(ctx, 1380, 880, 1.8, t=t, arm_l=0.9, arm_r=0.3)
        # funnel
        ctx.move_to(1100, 300); ctx.line_to(1260, 300); ctx.line_to(1205, 420); ctx.line_to(1155, 420); ctx.close_path()
        src(ctx, '#6b7fb8'); ctx.fill()
        # stack of drives
        for k in range(int(1 + 5 * prog(lt, l3 + 1.0, l3 + 7.0))):
            rrect(ctx, 1080, 800 - k * 56, 200, 46, 10); src(ctx, '#2f4aa8'); ctx.fill()
            circle(ctx, 1250, 823 - k * 56, 6, C['green'])
        # network on the left
        nodes = [(250, 300), (450, 200), (520, 420), (300, 560), (600, 650), (180, 760)]
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if (i + j) % 2 == 0:
                    ctx.move_to(*nodes[i]); ctx.line_to(*nodes[j])
        ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.25); ctx.stroke()
        for (x, y) in nodes: circle(ctx, x, y, 16, C['cyan'], 0.9)
        for k in range(14):
            ph = (t * 0.45 + k / 14) % 1
            sx, sy = nodes[k % len(nodes)]
            x = lerp(sx, 1180, ph); y = lerp(sy, 300, ph) - 120 * math.sin(math.pi * ph)
            packet(ctx, x, y, 0.6, col=[C['cyan'], C['pink'], C['yellow']][k % 3], a=prog(lt, l3 + 0.4, l3 + 0.8))
            lock_icon(ctx, x + 18, y - 18, 0.35)
        hourglass(ctx, 1660, 420, 1.0, t, a=prog(lt, l3 + 3.0, l3 + 3.4))
        pill(ctx, 1180, 200, 'SAVED FOR LATER', C['grey'], C['dark'], 34, prog(lt, l3 + 1.6, l3 + 2.0))
        hp = prog(lt, l3 + 5.4, l3 + 5.9)
        if hp > 0:
            rrect(ctx, 260, 60, 1400, 110, 30); src(ctx, '#05081a', 0.7 * hp); ctx.fill()
            rich(ctx, [('HARVEST NOW, ', C['white']), ('DECRYPT LATER', C['pink'])], 960, 115, 64, hp, maxw=1320)
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), harvest)


# ===================================================================== 5  BITCOIN
def s5(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = starts(L)
    bg(ctx, t, top='#120c2e', bot='#3a1f2a', glow_col='#7a3a1a', gy=560)

    def curve():
        pc = prog(lt, l0 + 0.2, l0 + 0.8)
        btc_coin(ctx, 620, 470, 200 * eback(pc), a=pc, sq=abs(math.cos(t * 1.2)) * 0.85 + 0.15)
        pe = prog(lt, l0 + 2.0, l0 + 4.5)
        if pe > 0:
            ctx.move_to(1000, 470); ctx.line_to(1740, 470); ctx.move_to(1130, 180); ctx.line_to(1130, 760)
            ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.35 * clamp(pe * 3)); ctx.stroke()
            elliptic(ctx, 1260, 470, 95, 30, prog_=pe, col=C['cyan'])
            rich(ctx, [('y^2 = x^3 + 7', C['cyan'])], 1480, 220, 44, clamp(pe * 2), pop=False)
            rich(ctx, [('elliptic-curve cryptography', C['white'])], 1370, 790, 38, prog(lt, l0 + 2.4, l0 + 2.9))
        pq = prog(lt, l0 + 5.6, l0 + 6.2)
        if pq > 0:
            glow(ctx, 1260, 470, 380, Q, 0.4 * pq * (0.7 + 0.3 * math.sin(t * 5)))
            pill(ctx, 1370, 120, 'BREAKABLE WITH SHOR', Q, C['white'], 38, pq)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), curve)

    def grid():
        red = [i for i in range(100) if random.Random(i * 7).random() < 0.3][:30]
        while len(red) < 30: red.append(len(red) * 3 + 1)
        for i in range(100):
            r_, c_ = divmod(i, 20)
            x = 260 + c_ * 70; y = 330 + r_ * 70
            pa = prog(lt, l1 + 0.2 + i * 0.012, l1 + 0.5 + i * 0.012)
            exposed = i in red and lt > l1 + 4.0 + red.index(i) * 0.06
            btc_coin(ctx, x, y, 28 * eback(pa), a=pa * (0.45 if not exposed and lt > l1 + 4 else 1.0))
            if exposed:
                circle(ctx, x, y, 34, C['red'], 0.35)
                padlock(ctx, x + 20, y - 22, 0.16, open_=1.0, body=C['red'])
        cnt = prog(lt, l1 + 0.6, l1 + 3.4)
        rich(ctx, [(f'{6.4 * eo(cnt):.1f} million BTC', BTC)], 960, 150, 76, prog(lt, l1 + 0.4, l1 + 0.8))
        pill(ctx, 960, 760, 'about 30% of all bitcoin: public key exposed', C['red'], C['white'], 36, prog(lt, l1 + 5.0, l1 + 5.4))
        source_line(ctx, 'Estimate: Quantum Alliance (Oct 2026)', prog(lt, l1 + 1.0, l1 + 1.4))
    fade_block(ctx, win(lt, l1 - 0.2, l2), grid)

    def satoshi():
        person(ctx, 520, 900, 2.1, mono='#0a0f2e', a=1.0)
        q = prog(lt, l2 + 0.6, l2 + 1.0)
        rich(ctx, [('?', C['yellow'])], 520, 380, 130, q)
        label(ctx, 'Satoshi Nakamoto', 520, 960, 40, C['grey'], q, w='normal')
        chest(ctx, 1260, 760, 1.9, open_=0.0, dust=prog(lt, l2 + 3.0, l2 + 4.0), t=t)
        pill(ctx, 1260, 200, '~1.1 MILLION BTC', BTC, C['dark'], 52, prog(lt, l2 + 1.6, l2 + 2.0))
        rich(ctx, [('untouched for 15+ years', C['grey'])], 1260, 290, 36, prog(lt, l2 + 3.6, l2 + 4.0), w='normal')
        source_line(ctx, 'Widely cited estimate', q)
    fade_block(ctx, win(lt, l2 - 0.2, l3), satoshi)

    def take():
        d = eo(prog(lt, l3 - 0.2, l3 + 0.9))
        qcomputer(ctx, 1500, -580 + 560 * d, 0.95, t, glow_a=1.0)
        op = prog(lt, l3 + 1.0, l3 + 1.5)
        chest(ctx, 760, 820, 1.9, open_=op, fill=1.0 - prog(lt, l3 + 1.4, l3 + 3.2), t=t)
        if op > 0:
            for k in range(16):
                st = l3 + 1.3 + k * 0.11
                ph = clamp((lt - st) / 1.3)
                if ph <= 0: continue
                x = lerp(760 + (k % 5 - 2) * 40, 1500, ss(ph)); y = lerp(640, 470, ph) - 260 * math.sin(math.pi * ph)
                btc_coin(ctx, x, y, 34 * (1 - 0.6 * ph), a=1 - ph ** 4, rot=ph * 3)
            beam = clamp(op * 2)
            ctx.move_to(1500, 520); ctx.line_to(800, 650); ctx.set_line_width(40 * beam); src(ctx, Q, 0.25 * beam); ctx.stroke()
        pill(ctx, 760, 200, 'TAKEN', C['red'], C['white'], 60, prog(lt, l3 + 2.2, l3 + 2.6))
    te = L[3][1]
    fade_block(ctx, win(lt, l3 - 0.2, l4), take)

    def freeze():
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        bg(ctx, t, top='#0a2a5a', bot='#1a4a8a', glow_col='#3ab0ff', gx=480, gy=520)
        for k in range(6):
            btc_coin(ctx, 330 + (k % 3) * 150, 520 + (k // 3) * 150, 60)
        ice_block(ctx, 480, 600, 560, 380, prog(lt, l4 + 0.6, l4 + 1.2))
        rich(ctx, [('FREEZE THEM?', C['cyan'])], 480, 200, 80, prog(lt, l4 + 0.4, l4 + 0.8))
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        bg(ctx, t, top='#2a1028', bot='#4a1f2a', glow_col='#a03a3a', gx=1440, gy=520)
        tp = prog(lt, l4 + 2.6, l4 + 3.0)
        rrect(ctx, 1220, 360, 440, 480, 40); src(ctx, '#9a94a8', tp); ctx.fill()
        rich(ctx, [('NO ONE CAN', C['dark'])], 1440, 470, 44, tp, pop=False, shadow=False)
        rich(ctx, [('TAKE', C['dark'])], 1440, 550, 60, tp, pop=False, shadow=False)
        rich(ctx, [('YOUR COINS', C['dark'])], 1440, 630, 44, tp, pop=False, shadow=False)
        cr = prog(lt, l4 + 4.0, l4 + 4.6)
        if cr > 0:
            pts = [(1380, 360), (1420, 450), (1390, 520), (1460, 600), (1430, 700), (1480, 840)]
            n = 1 + int(cr * (len(pts) - 1))
            ctx.move_to(*pts[0])
            for p in pts[1:n + 1]: ctx.line_to(*p)
            ctx.set_line_width(8); src(ctx, '#2a1f3a'); ctx.stroke()
        rich(ctx, [("BITCOIN'S SACRED RULE", C['pink'])], 1440, 200, 60, prog(lt, l4 + 2.4, l4 + 2.8), maxw=860)
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    fade_block(ctx, prog(lt, l4 - 0.2, l4 + 0.3), freeze)


# ===================================================================== 6  NEW LOCKS
def s6(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#06203a', bot='#0c3a5a', glow_col='#1a8a9a', gy=560)

    def newlock():
        p = prog(lt, l0 + 0.4, l0 + 1.0)
        padlock(ctx, 640, 580, 2.5 * eback(p), body=C['cyan'], lattice=True, t=t)
        glow(ctx, 640, 580, 400, C['cyan'], 0.3 * p)
        label(ctx, 'NEW LOCKS', 640, 120, 70, C['cyan'], p)
        ps = prog(lt, l0 + 3.0, l0 + 3.5)
        shield(ctx, 1320, 380, 1.3 * eback(ps), col=C['green'])
        label(ctx, 'NIST · August 2024', 1320, 580, 44, C['white'], ps)
        for k, txt in enumerate(('FIPS 203', 'FIPS 204', 'FIPS 205')):
            st = l0 + 4.4 + k * 0.4
            pill(ctx, 1120 + k * 200, 690, txt, C['green'], C['dark'], 32, prog(lt, st, st + 0.3))
        rich(ctx, [('first post-quantum standards', C['grey'])], 1320, 790, 34, prog(lt, l0 + 5.2, l0 + 5.6), w='normal')
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), newlock)

    def lattice():
        pa = prog(lt, l1 + 0.1, l1 + 0.6)
        ox, oy = 560, 500
        for i in range(-6, 7):
            for j in range(-4, 5):
                x = ox + i * 80 + j * 34; y = oy + j * 70
                if 120 < x < 1100 and 160 < y < 840:
                    circle(ctx, x, y, 7, C['cyan'], pa * (0.5 + 0.3 * math.sin(t * 2 + i * 0.5 + j)))
        ctx.move_to(ox, oy); ctx.line_to(ox + 80 + 34, oy + 70); ctx.set_line_width(6); src(ctx, C['yellow'], prog(lt, l1 + 1.2, l1 + 1.6)); ctx.stroke()
        rich(ctx, [('lattice math', C['cyan'])], 560, 140, 56, pa)
        qcomputer(ctx, 1480, 80, 0.75, t, a=pa, glow_a=0.6)
        for k in range(4):
            ph = (t * 0.7 + k / 4) % 1
            rich(ctx, [('?', C['yellow'])], 1300 + k * 90, 560 - ph * 200, 70, (1 - ph) * prog(lt, l1 + 1.6, l1 + 2.0), pop=False)
        pill(ctx, 1480, 860, 'believed to resist quantum attacks', C['green'], C['dark'], 32, prog(lt, l1 + 2.4, l1 + 2.8))
    fade_block(ctx, win(lt, l1 - 0.2, l2), lattice)

    def tl():
        y = 520
        pl = prog(lt, l2 + 0.1, l2 + 0.8)
        ctx.move_to(200, y); ctx.line_to(200 + 1520 * pl, y); ctx.set_line_width(10); src(ctx, C['white'], 0.7); ctx.stroke()
        marks = [(2024, 'standards published', C['green'], l2 + 0.4), (2029, "Google's own deadline", C['cyan'], l2 + 3.4),
                 (2030, 'NIST: start phasing out', C['yellow'], l2 + 1.0), (2035, 'NIST: old locks retired', C['pink'], l2 + 1.8)]
        for k, (yr, lab, col, st) in enumerate(marks):
            x = 260 + (yr - 2024) * 130
            p = prog(lt, st, st + 0.4)
            if p <= 0: continue
            circle(ctx, x, y, 22 * eback(p), col)
            up = k % 2 == 0
            rich(ctx, [(str(yr), col)], x, y + (-70 if up else 70), 52, p)
            rich(ctx, [(lab, C['white'])], x, y + (-140 if up else 140), 32, p, w='normal', maxw=330)
        rich(ctx, [('NIST dates are a proposal (draft, 2024)', C['grey'])], 960, 880, 28, prog(lt, l2 + 2.2, l2 + 2.6), w='normal', pop=False)
        label(ctx, 'THE DEADLINES', 960, 130, 64, C['white'], prog(lt, l2, l2 + 0.4))
    fade_block(ctx, win(lt, l2 - 0.2, l3), tl)

    def swap():
        devs = ['bank', 'phone', 'laptop', 'server', 'atm', 'monitor', 'bulb', 'truck']
        for k, d in enumerate(devs):
            cx = 280 + (k % 4) * 450; cy = 370 + (k // 4) * 340
            pa = prog(lt, l3 + 0.1 + k * 0.12, l3 + 0.5 + k * 0.12)
            def dv(d=d, cx=cx, cy=cy):
                if d == 'bank': bank(ctx, cx, cy + 110, 0.6)
                elif d == 'phone': phone(ctx, cx, cy, 0.55, screen=C['cyan'])
                elif d == 'laptop': laptop(ctx, cx, cy + 70, 0.9, t=t)
                elif d == 'server': server(ctx, cx, cy + 130, 0.85, t=t)
                elif d == 'atm': atm(ctx, cx, cy + 130, 0.8, t=t)
                elif d == 'monitor': monitor(ctx, cx, cy + 90, 1.0, screen=C['cyan'])
                elif d == 'bulb': bulb(ctx, cx, cy - 20, 0.9, t)
                else: truck(ctx, cx, cy + 70, 0.5, t=t)
            pop_scale(ctx, cx, cy, pa, dv)
            sw = prog(lt, l3 + 1.8 + k * 0.55, l3 + 2.2 + k * 0.55)
            padlock(ctx, cx + 120, cy - 90, 0.5 * eback(pa), body=lerp_col(C['yellow'], C['cyan'], sw), lattice=sw > 0.5, t=t)
        pb = prog(lt, l3 + 1.0, l3 + 1.4)
        rrect(ctx, 460, 900 - 30, 1000, 30, 15); src(ctx, '#1d2c6e', pb); ctx.fill()
        rrect(ctx, 460, 900 - 30, 30 + 400 * prog(lt, l3 + 1.8, l3 + 7.0), 30, 15); src(ctx, C['cyan'], pb); ctx.fill()
        label(ctx, 'changing every lock on the internet', 960, 100, 54, C['white'], prog(lt, l3 + 0.2, l3 + 0.6))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), swap)


# ===================================================================== 7  WHEN?
def s7(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#0b1640', bot='#2a1f6a', glow_col='#4a3aa8', gy=600)

    def when():
        y = 560
        ctx.move_to(200, y); ctx.line_to(1720, y); ctx.set_line_width(8); src(ctx, C['white'], 0.6); ctx.stroke()
        for k, yr in enumerate(range(2026, 2037)):
            x = 240 + k * 144
            p = prog(lt, l0 + 0.3 + k * 0.06, l0 + 0.6 + k * 0.06)
            circle(ctx, x, y, 10, C['white'], p)
            rich(ctx, [(str(yr), C['grey'])], x, y + 50, 30, p, w='normal', pop=False)
        hb = prog(lt, l0 + 3.4, l0 + 4.0)
        if hb > 0:
            x0 = 240 + 2 * 144; x1 = 240 + 5 * 144
            rrect(ctx, x0 - 20, y - 70, (x1 - x0 + 40) * eo(hb), 140, 30); src(ctx, C['yellow'], 0.25); ctx.fill()
            rich(ctx, [('most estimates', C['yellow'])], (x0 + x1) / 2, y - 120, 40, hb)
        pa = prog(lt, l0 + 0.2, l0 + 0.6)
        rich(ctx, [('WHEN IS Q-DAY?', C['white'])], 960, 170, 80, pa)
        for k in range(5):
            ph = (t * 0.35 + k / 5) % 1
            rich(ctx, [('?', Q)], 300 + k * 330, 820 - 140 * ph, 70, (1 - ph) * pa, pop=False)
        rich(ctx, [('Nobody knows.', C['grey'])], 960, 270, 44, prog(lt, l0 + 1.4, l0 + 1.8), w='normal')
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), when)

    def good():
        qcomputer(ctx, 960, -120, 0.9, t, glow_a=0.8)
        items = [(420, 'new medicines', 'pill'), (960, 'new materials', 'mat'), (1500, 'simulate nature', 'mol')]
        for k, (x, lab, kind) in enumerate(items):
            st = l1 + 1.0 + k * 1.2
            p = prog(lt, st, st + 0.5)
            def ic(x=x, kind=kind):
                card(ctx, x - 190, 520, 380, 340, '#20307e', 40)
                if kind == 'pill':
                    ctx.save(); ctx.translate(x, 670); ctx.rotate(-0.6)
                    rrect(ctx, -110, -42, 220, 84, 42); src(ctx, C['white']); ctx.fill()
                    ctx.rectangle(0, -42, 110, 84); ctx.clip(); rrect(ctx, -110, -42, 220, 84, 42); src(ctx, C['pink']); ctx.fill()
                    ctx.restore()
                elif kind == 'mat':
                    for i in range(4):
                        for j in range(3):
                            circle(ctx, x - 120 + i * 80, 610 + j * 60, 18, C['cyan'] if (i + j) % 2 else C['yellow'])
                else: molecule(ctx, x, 680, 0.8, t)
            pop_scale(ctx, x, 690, p, ic)
            label(ctx, lab, x, 910, 40, C['white'], p)
    fade_block(ctx, win(lt, l1 - 0.2, l2), good)

    def race():
        hills(ctx, 860, '#1a2766', amp=0)
        fx = 1640
        ctx.move_to(fx, 860); ctx.line_to(fx, 360); ctx.set_line_width(10); src(ctx, C['white']); ctx.stroke()
        for i in range(4):
            for j in range(3):
                ctx.rectangle(fx + i * 30, 360 + j * 30, 30, 30); src(ctx, C['white'] if (i + j) % 2 == 0 else C['dark']); ctx.fill()
        rich(ctx, [('Q-DAY', C['yellow'])], fx, 300, 50, 1.0, pop=False)
        p = ss(prog(lt, l2 + 0.2, l2 + 5.6))
        bob = abs(math.sin(t * 9)) * 14
        x1 = lerp(240, 1340, p); x2 = lerp(240, 1260, p ** 1.1)
        person(ctx, x1, 860 - bob, 1.3, shirt=C['orange'], arm_l=0.9 * math.sin(t * 9), arm_r=-0.9 * math.sin(t * 9))
        padlock(ctx, x1 + 60, 640 - bob, 0.45, body=C['cyan'], lattice=True, t=t)
        rich(ctx, [('new locks', C['cyan'])], x1, 520, 32, 1.0, pop=False)
        bot(ctx, x2 - 160, 860 - abs(math.sin(t * 9 + 1)) * 14, 1.3, t=t, arm_l=0.9 * math.sin(t * 9 + 1), arm_r=-0.9 * math.sin(t * 9 + 1), eye=Q)
        glow(ctx, x2 - 160, 700, 160, Q, 0.4)
        rich(ctx, [('quantum computers', Q)], x2 - 160, 960, 32, 1.0, pop=False)
        label(ctx, 'THE REAL RACE', 960, 130, 70, C['white'], prog(lt, l2, l2 + 0.4))
    fade_block(ctx, win(lt, l2 - 0.2, l3), race)

    def finale():
        night_bg(ctx, t, glow_col='#2a2a6a')
        city(ctx, 900, t, 0.9, seed=44)
        hills(ctx, 940, '#0a1035', amp=0)
        te = L[3][1]
        pf = prog(lt, te + 0.4, te + 0.9)
        alarm_clock(ctx, 960, 470, 1.6, t, ring=0, a=1 - pf)
        if pf < 0.5: x_mark(ctx, 960, 470, 90, prog(lt, l3 + 1.4, l3 + 1.9), col=C['pink'])
        if pf > 0:
            ctx.set_source_rgba(0.02, 0.03, 0.12, 0.6 * pf); ctx.paint()
            rich(ctx, [('Q-DAY', C['pink'])], 960, 420, 170, pf)
            rich(ctx, [('Will we be ready?', C['white'])], 960, 590, 64, prog(lt, te + 1.2, te + 1.7), w='normal')
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), finale)
