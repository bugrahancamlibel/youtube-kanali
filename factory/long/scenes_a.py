from base import *

# ===================================================================== 0  COLD OPEN
MINI = [(i, j) for j in range(4) for i in range(10)]


def mini_face(ctx, cx, cy, s, k, t, gl=0.0):
    L = LOOKS[k % len(LOOKS)]
    face(ctx, cx, cy, s, L, 1.0 if (t * 0.9 + k * 0.37) % 3.3 < 0.1 else 0.0)


def s0(ctx, lt, t, L):
    bg(ctx, t, glow_col='#4a2a9a', gy=560)
    l0, l1, l2, l3, l4 = [a for a, b in L]
    end4 = L[4][1]
    # ---- the two cards (lines 0-2)
    out = ss(prog(lt, l3 - 0.1, l3 + 0.6))
    if out < 1:
        for k, (cx0, Lk) in enumerate(((620, LOOKS[3]), (1300, LOOKS[2]))):
            p = eback(prog(lt, 0.15 + 0.15 * k, 0.65 + 0.15 * k), 1.3)
            if p <= 0: continue
            cx = cx0 + (-1 if k == 0 else 1) * 900 * ss(out)
            x0, y0, cw, chh = cx - 230, 190, 460, 600
            gl = math.sin(math.pi * prog(lt, l2 + 0.2, l2 + 0.75))

            def draw(c, x0=x0, Lk=Lk, cx=cx, k=k):
                card(c, x0, y0, cw, chh, '#23347f', 44)
                c.save(); rrect(c, x0, y0, cw, chh, 44); c.clip()
                glow(c, cx, 470, 380, Lk['shirt'], 0.35)
                face(c, cx, 480, 0.9, Lk, 1.0 if (lt + k * 0.9) % 2.9 < 0.11 else 0.0)
                c.restore()
                circle(c, cx, y0 + chh, 44, C['white'])
                rich(c, [('AB'[k], C['dark'])], cx, y0 + chh - 2, 50, pop=False, shadow=False)
            ctx.save(); ctx.translate(cx, 490); ctx.scale(p, p); ctx.translate(-cx, -490)
            glitched(ctx, draw, x0 - 20, y0 - 20, cw + 40, chh + 90, gl, int(t * 30) + k * 77)
            ctx.restore()
            wire(ctx, cx, 480, 0.9, prog(lt, l2 + 0.5, l2 + 1.0) * (1 - out), t)
            # question / verdict tags
            q = prog(lt, l1 + 0.3 + 0.4 * k, l1 + 0.6 + 0.4 * k) * (1 - prog(lt, l2, l2 + 0.25))
            pill(ctx, cx, 150, ['REAL?', 'FAKE?'][k], [C['green'], C['red']][k], C['white'], 38, q * (1 - out))
            pill(ctx, cx, 150, 'AI-MADE', C['pink'], C['white'], 38, prog(lt, l2 + 0.6 + 0.12 * k, l2 + 0.9 + 0.12 * k) * (1 - out))
        if lt < l2 + 0.3:
            title(ctx, [('VS', C['grey'])], 490, 60, prog(lt, 0.6, 0.9) * (1 - prog(lt, l2, l2 + 0.3)))
    # ---- line 3: voices, calls, video
    pin = prog(lt, l3 + 0.3, l3 + 0.7); pout = ss(prog(lt, l4 - 0.2, l4 + 0.4))
    if pin > 0 and pout < 1:
        icons = [('VOICES', C['cyan']), ('PHONE CALLS', C['yellow']), ('LIVE VIDEO', C['pink'])]
        for k, (lab, col) in enumerate(icons):
            p = prog(lt, l3 + 0.6 + k * 0.55, l3 + 1.0 + k * 0.55)
            if p <= 0: continue
            cx = 480 + k * 480; cy = 470 - 700 * pout

            def draw(c, k=k, cx=cx, cy=cy, col=col):
                card(c, cx - 190, cy - 210, 380, 420, '#20307e', 44)
                glow(c, cx, cy - 20, 200, col, 0.4)
                if k == 0:
                    wave_bars(c, cx - 140, cy - 20, 20, 14.5, 150, t, col, seed=1)
                elif k == 1:
                    phone(c, cx, cy - 20, 0.55, a=1.0, ring=1.0, t=t)
                else:
                    rrect(c, cx - 150, cy - 120, 300, 190, 22); src(c, '#0f1640'); c.fill()
                    face(c, cx, cy - 60, 0.4, LOOKS[5])
                    circle(c, cx + 115, cy - 95, 10, C['red'], 0.6 + 0.4 * math.sin(t * 8))
                rich(c, [(lab, col)], cx, cy + 160, 40, pop=False)
            g = 0.9 * max(0, math.sin(t * 7 + k * 2)) ** 30
            ctx.save(); ctx.translate(cx, cy); s = eback(p); ctx.scale(s, s); ctx.translate(-cx, -cy)
            glitched(ctx, draw, cx - 210, cy - 230, 420, 460, g, int(t * 30) + k)
            ctx.restore()
            pill(ctx, cx + 120, cy - 200, 'FAKE', C['red'], C['white'], 30, prog(lt, l3 + 1.2 + k * 0.55, l3 + 1.45 + k * 0.55) * (1 - pout))
    # ---- line 4: wall of faces then title
    pw = prog(lt, l4 + 0.1, l4 + 1.0)
    tt = prog(lt, end4 + 0.2, end4 + 0.6)
    if pw > 0:
        sp = 196
        for n, (i, j) in enumerate(MINI):
            cx, cy = 96 + i * sp - 0, 150 + j * 260 + 60
            d = math.hypot(i - 4.5, j - 1.5)
            p = eback(prog(lt, l4 + 0.1 + d * 0.08, l4 + 0.5 + d * 0.08))
            if p <= 0: continue
            fade = 1 - 0.75 * tt
            g = 1.0 if math.sin(t * 3 + n * 1.7) > 0.985 else 0.0

            def draw(c, cx=cx, cy=cy, n=n):
                rrect(c, cx - 86, cy - 120, 172, 230, 26); src(c, '#22337d'); c.fill()
                c.save(); rrect(c, cx - 86, cy - 120, 172, 230, 26); c.clip()
                mini_face(c, cx, cy - 15, 0.36, n, t); c.restore()
            ctx.save(); ctx.translate(cx, cy); ctx.scale(p, p); ctx.translate(-cx, -cy)
            ctx.push_group(); glitched(ctx, draw, cx - 100, cy - 130, 200, 250, g, n + int(t * 30))
            ctx.pop_group_to_source(); ctx.paint_with_alpha(fade); ctx.restore()
    if tt > 0:
        ctx.set_source_rgba(0.03, 0.05, 0.16, 0.6 * tt); ctx.paint()
        title(ctx, [('YOU CAN NO LONGER', C['white'])], 440, 92, tt)
        g = math.sin(math.pi * prog(lt, end4 + 0.7, end4 + 1.0))

        def draw(c):
            rich(c, [('TRUST YOUR EYES', C['cyan'])], W / 2, 590, 170, 1, maxw=1700, pop=False)
        p2 = prog(lt, end4 + 0.45, end4 + 0.85)
        if p2 > 0:
            ctx.save(); ctx.translate(W / 2, 590); s = eback(p2); ctx.scale(s, s); ctx.translate(-W / 2, -590)
            glitched(ctx, draw, 80, 470, 1760, 250, g * 0.8, int(t * 30)); ctx.restore()


# ===================================================================== 1  THE DUEL
NET = [[(1150, 300 + 160 * i) for i in range(4)], [(1400, 230 + 150 * i) for i in range(5)],
       [(1650, 380 + 160 * i) for i in range(2)]]


def quality_face(ctx, cx, cy, s, q, L, t, seed=0):
    block = lerp(70, 1, q ** 0.8)
    w, h = 420 * s / 0.9, 520 * s / 0.9

    def draw(c):
        face(c, cx, cy, s, L, 0.0, smile=lerp(-0.6, 1.0, q))
        rnd = random.Random(seed + int(q * 12))
        for _ in range(int(14 * (1 - q))):
            circle(c, cx + rnd.uniform(-120, 120) * s, cy + rnd.uniform(-150, 150) * s, rnd.uniform(12, 40) * s,
                   rnd.choice([C['pink'], C['green'], '#7a4a2a', C['cyan']]), 0.7 * (1 - q))
    pixelate_region(ctx, draw, cx - w / 2, cy - h * 0.42, w, h, block)


def s1(ctx, lt, t, L):
    bg(ctx, t, glow_col='#26408f', gy=600)
    l0, l1, l2, l3, l4 = [a for a, b in L]
    # ---- line 0: 2014 + network
    a0 = 1 - ss(prog(lt, l1 - 0.3, l1 + 0.2))
    if a0 > 0:
        ctx.push_group()
        rich(ctx, [('2014', C['yellow'])], 520, 420, 230, prog(lt, 0.3, 0.6))
        rich(ctx, [('Generative', C['white'])], 520, 600, 62, prog(lt, l0 + 1.2, l0 + 1.45))
        rich(ctx, [('Adversarial', C['pink'])], 520, 680, 62, prog(lt, l0 + 1.4, l0 + 1.65))
        rich(ctx, [('Network', C['white'])], 520, 760, 62, prog(lt, l0 + 1.6, l0 + 1.85))
        pn = prog(lt, 0.5, 1.4)
        for li in range(2):
            for (x0, y0) in NET[li]:
                for (x1, y1) in NET[li + 1]:
                    ctx.move_to(x0, y0); ctx.line_to(lerp(x0, x1, pn), lerp(y0, y1, pn))
        ctx.set_line_width(3); src(ctx, C['grey'], 0.35); ctx.stroke()
        for li in range(2):
            for a_, (x0, y0) in enumerate(NET[li]):
                for b_, (x1, y1) in enumerate(NET[li + 1]):
                    ph = (t * 0.8 + a_ * 0.31 + b_ * 0.17 + li * 0.5) % 1
                    if pn >= 1: circle(ctx, lerp(x0, x1, ph), lerp(y0, y1, ph), 5, C['cyan'], 0.8)
        for li, layer in enumerate(NET):
            for k, (x, y) in enumerate(layer):
                p = eback(prog(lt, 0.4 + li * 0.25 + k * 0.05, 0.7 + li * 0.25 + k * 0.05))
                if p > 0:
                    glow(ctx, x, y, 60, [C['cyan'], C['pink'], C['yellow']][li], 0.5)
                    circle(ctx, x, y, 26 * p, [C['cyan'], C['pink'], C['yellow']][li])
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a0)
    if lt < l1 - 0.3: return
    # ---- robots
    rin = eo(prog(lt, l1 + 0.1, l1 + 0.9))
    rout = ss(prog(lt, l4 - 0.2, l4 + 0.5))
    fx = lerp(-300, 400, rin) - 700 * rout
    dx = lerp(2220, 1520, rin) + 700 * rout
    q = 0.08 + 0.92 * ss(prog(lt, l3 + 0.5, L[3][1] - 0.4)) ** 1.6
    painting = l2 < lt < L[3][1]
    arm = 0.35 * math.sin(t * 9) if painting else 0
    caught = (l2 + 1.4 < lt < L[3][1] - 0.6)
    robot2(ctx, fx, 860, 1.0, '#c24a8a', C['pink'], 'forger', t, talk=0.0, look=0.6, arm=arm)
    robot2(ctx, dx, 860, 1.0, '#2f6fb0', C['cyan'], 'detective', t, talk=1.0 if caught else 0.0, look=-0.6,
           arm=0.25 * math.sin(t * 2))
    pill(ctx, fx, 330, 'FORGER', C['pink'], C['white'], 36, prog(lt, l1 + 1.6, l1 + 1.9) * (1 - rout))
    pill(ctx, dx, 330, 'DETECTIVE', C['cyan'], C['dark'], 36, prog(lt, l1 + 2.7, l1 + 3.0) * (1 - rout))
    vs = prog(lt, l1 + 3.2, l1 + 3.5) * (1 - prog(lt, l2 - 0.2, l2 + 0.1))
    title(ctx, [('VS', C['yellow'])], 520, 150, vs)
    # easel + canvas
    pe = eback(prog(lt, l2 - 0.1, l2 + 0.4)) * (1 - rout)
    if pe > 0:
        def easel():
            ctx.set_line_width(16); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, '#8c6a45')
            ctx.move_to(900, 820); ctx.line_to(960, 220); ctx.line_to(1020, 820); ctx.move_to(960, 300); ctx.line_to(960, 900)
            ctx.stroke()
            rrect(ctx, 760, 220, 400, 470, 18); src(ctx, '#f4efe6'); ctx.fill()
            ctx.save(); rrect(ctx, 772, 232, 376, 446, 12); ctx.clip()
            src(ctx, '#2a3a7a'); ctx.paint()
            quality_face(ctx, 960, 470, 0.72, q, LOOKS[1], t, 3)
            ctx.restore()
        pop_scale(ctx, 960, 560, pe, easel)
    # round counter
    pr = prog(lt, l3 - 0.2, l3 + 0.2) * (1 - rout)
    if pr > 0:
        n = 1 + (1_000_000 - 1) * ss(prog(lt, l3 + 0.3, L[3][1] - 0.4)) ** 3
        title(ctx, [('ROUND ', C['grey']), (counter_text(n), C['white'])], 120, 64, pr, pop=False)
    # detective verdicts
    if caught:
        k = int((lt - l2 - 1.4) / 0.9)
        pb = prog((lt - l2 - 1.4) % 0.9, 0, 0.2)
        bubble(ctx, dx - 190, 190, 'FAKE!', C['red'], pb)
    if L[3][1] - 0.6 < lt < l4:
        bubble(ctx, dx - 190, 190, '...real?', C['yellow'], prog(lt, L[3][1] - 0.6, L[3][1] - 0.35))
        rich(ctx, [('?', C['yellow'])], dx + 130, 250 + 10 * math.sin(t * 5), 90, 1)
    # ---- line 4: the name
    if lt > l4 - 0.1:
        pc = eback(prog(lt, l4 + 0.2, l4 + 0.7))
        def post():
            card(ctx, 560, 300, 800, 330, '#f4f6ff', 30, stroke=False)
            circle(ctx, 640, 380, 34, C['orange'])
            rich(ctx, [('u/deepfakes', C['dark'])], 700, 368, 40, pop=False, align='left', shadow=False)
            rich(ctx, [('posted in 2017', '#6b7fb8')], 700, 412, 30, pop=False, align='left', shadow=False, w='normal')
            for i, wl in enumerate((620, 560, 420)):
                rrect(ctx, 610, 470 + i * 42, wl, 18, 9); src(ctx, '#c9d2f0'); ctx.fill()
            ctx.move_to(1290, 400); ctx.line_to(1320, 360); ctx.line_to(1350, 400); ctx.close_path(); src(ctx, C['orange'])
            ctx.fill()
        pop_scale(ctx, 960, 470, pc, post)
        pw = prog(lt, l4 + 2.4, l4 + 2.7)
        rich(ctx, [('DEEP', C['cyan']), (' learning', C['grey'])], 700, 780, 64, pw, w='bold')
        rich(ctx, [('+', C['white'])], 960, 780, 64, prog(lt, l4 + 2.6, l4 + 2.8))
        rich(ctx, [('FAKE', C['pink'])], 1150, 780, 64, prog(lt, l4 + 2.75, l4 + 3.0))
        stamp(ctx, 960, 900, 'DEEPFAKES', C['yellow'], prog(lt, L[4][1] - 0.4, L[4][1] - 0.1), rot=-0.05, size=90)


# ===================================================================== 2  HOW GOOD IT GOT
WIN2 = {(13, 7), (31, 34)}


def s2(ctx, lt, t, L):
    bg(ctx, t, glow_col='#3a2a8a', gy=560)
    l0, l1, l2, l3, l4 = [a for a, b in L]
    # ---- line 0: realism chart
    a0 = 1 - ss(prog(lt, l1 - 0.3, l1 + 0.1))
    if a0 > 0:
        ctx.push_group()
        x0, x1, y0, y1 = 260, 1660, 860, 230
        pa = prog(lt, 0.2, 0.7)
        ctx.move_to(x0, y1 - 20); ctx.line_to(x0, y0); ctx.line_to(x0 + (x1 - x0 + 60) * pa, y0)
        ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['grey']); ctx.stroke()
        rich(ctx, [('realism', C['grey'])], x0 + 10, y1 - 60, 36, pa, align='left', pop=False, w='normal')
        years = [2014, 2017, 2020, 2023, 2026]
        pc = prog(lt, 0.6, 2.4)
        ctx.new_path()
        for i in range(101):
            u = i / 100
            if u > pc: break
            x = lerp(x0, x1, u); y = lerp(y0 - 30, y1, u ** 3.2)
            (ctx.move_to if i == 0 else ctx.line_to)(x, y)
        ctx.set_line_width(10); src(ctx, C['pink']); ctx.stroke()
        for k, yr in enumerate(years):
            u = k / 4
            x = lerp(x0, x1, u); y = lerp(y0 - 30, y1, u ** 3.2)
            p = prog(pc, u - 0.02, u + 0.06) if pc < 1 else 1
            rich(ctx, [(str(yr), C['white'])], x, y0 + 50, 38, prog(lt, 0.4 + k * 0.1, 0.7 + k * 0.1), pop=False)
            if p > 0:
                cy = y - 140
                bx = 150
                def draw(c, x=x, cy=cy):
                    rrect(c, x - bx / 2, cy - 90, bx, 180, 18); src(c, '#22337d'); c.fill()
                    c.save(); rrect(c, x - bx / 2, cy - 90, bx, 180, 18); c.clip()
                    quality_face(c, x, cy - 10, 0.3, [0.05, 0.3, 0.6, 0.85, 1.0][k], LOOKS[k], t, k); c.restore()
                pop_scale(ctx, x, cy, p, lambda d=draw: d(ctx))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a0)
    # ---- lines 1-2: 2000 people
    if l1 - 0.3 < lt < l3 + 0.3:
        a1 = prog(lt, l1 - 0.2, l1 + 0.2) * (1 - prog(lt, l3 - 0.2, l3 + 0.2))
        ctx.push_group()
        rich(ctx, [('2025 study', C['grey'])], 120, 330, 44, prog(lt, l1, l1 + 0.3), align='left', w='normal')
        rich(ctx, [('2,000', C['cyan'])], 120, 450, 150, prog(lt, l1 + 0.2, l1 + 0.5), align='left')
        rich(ctx, [('people', C['white'])], 120, 570, 64, prog(lt, l1 + 0.4, l1 + 0.7), align='left')
        rich(ctx, [('real or fake?', C['grey'])], 120, 650, 44, prog(lt, l1 + 1.5, l1 + 1.8), align='left', w='normal')
        gx0, gy0, sp = 880, 175, 18.2
        for r in range(40):
            ap = prog(lt, l1 + 0.3 + r * 0.03, l1 + 0.5 + r * 0.03)
            if ap <= 0: continue
            for c in range(50):
                x, y = gx0 + c * sp, gy0 + r * sp
                win = (r, c) in WIN2
                red = prog(lt, l2 - 0.5 + (r + c) * 0.012, l2 - 0.35 + (r + c) * 0.012)
                if win and lt > l2 + 0.6: continue
                circle(ctx, x, y, 6.5, lerp_col('#3a4fa8', C['red'], 0 if win else red), ap)
        if lt > l2 + 0.6:
            p = eback(prog(lt, l2 + 0.6, l2 + 0.9))
            for (r, c) in WIN2:
                x, y = gx0 + c * sp, gy0 + r * sp
                for k in range(2):
                    ph = ((lt - l2) * 0.9 + k * 0.5) % 1
                    ctx.new_path(); ctx.arc(x, y, 10 + ph * 90, 0, 2 * math.pi); ctx.set_line_width(4)
                    src(ctx, C['green'], (1 - ph) * 0.8); ctx.stroke()
                glow(ctx, x, y, 80, C['green'], 0.8); circle(ctx, x, y, 13 * p, C['green'])
            rich(ctx, [('Only ', C['white']), ('2', C['green']), (' spotted', C['white'])], 120, 800, 64,
                 prog(lt, l2 + 0.7, l2 + 1.0), align='left')
            rich(ctx, [('every fake. ', C['white']), ('0.1%', C['green'])], 120, 880, 64, prog(lt, l2 + 0.9, l2 + 1.2),
                 align='left')
        source_line(ctx, 'Source: iProov deepfake detection study, 2025 (UK & US)', 1)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a1)
    # ---- line 3: AI faces judged more human
    if l3 - 0.3 < lt < l4 + 0.3:
        a3 = prog(lt, l3 - 0.2, l3 + 0.2) * (1 - prog(lt, l4 - 0.2, l4 + 0.2))
        ctx.push_group()
        for k, (cx, lab, col, hgt, Lk) in enumerate(((620, 'AI-GENERATED', C['pink'], 0.82, LOOKS[5]),
                                                       (1300, 'REAL PHOTO', C['cyan'], 0.58, LOOKS[0]))):
            p = eback(prog(lt, l3 + 0.1 + k * 0.2, l3 + 0.5 + k * 0.2))
            def draw(cx=cx, Lk=Lk, lab=lab, col=col):
                card(ctx, cx - 200, 260, 400, 500, '#23347f', 40)
                ctx.save(); rrect(ctx, cx - 200, 260, 400, 500, 40); ctx.clip()
                glow(ctx, cx, 500, 320, Lk['shirt'], 0.3); face(ctx, cx, 500, 0.8, Lk); ctx.restore()
                pill(ctx, cx, 260, lab, col, C['white'] if k == 0 else C['dark'], 32, 1)
            pop_scale(ctx, cx, 510, p, draw)
            bh = 300 * hgt * ss(prog(lt, l3 + 1.2, l3 + 2.6))
            bx = cx + 250
            rrect(ctx, bx, 760 - 300, 60, 300, 20); ctx.set_source_rgba(1, 1, 1, 0.08 * p); ctx.fill()
            if bh > 1:
                rrect(ctx, bx, 760 - bh, 60, bh, 20); src(ctx, col); ctx.fill()
        title(ctx, [('"Looks human!"', C['yellow'])], 150, 70, prog(lt, l3 + 1.0, l3 + 1.3))
        title(ctx, [('AI faces were judged human ', C['white']), ('more often', C['pink']), (' than real ones', C['white'])],
              815, 52, prog(lt, l3 + 2.0, l3 + 2.3))
        source_line(ctx, 'Source: Miller et al., Psychological Science, 2023 (study of White faces)', 1)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a3)
    # ---- line 4: voice clone
    if lt > l4 - 0.3:
        a4 = prog(lt, l4 - 0.2, l4 + 0.2)
        ctx.push_group()
        person(ctx, 300, 760, 1.6, shirt=C['orange'])
        wave_bars(ctx, 470, 520, 34, 17, 230, t, C['cyan'], seed=2, grow=prog(lt, l4 + 0.2, l4 + 1.0))
        pb = prog(lt, l4 + 1.1, l4 + 1.35)
        if pb > 0:
            ctx.move_to(466, 360); ctx.line_to(466, 340); ctx.line_to(470 + 10 * 17, 340); ctx.line_to(470 + 10 * 17, 360)
            ctx.set_line_width(6); src(ctx, C['yellow'], pb); ctx.stroke()
            pill(ctx, 470 + 5 * 17, 290, '3 seconds', C['yellow'], C['dark'], 36, pb)
            for i in range(10):
                pass
        fp = ss(prog(lt, l4 + 1.5, l4 + 2.2))
        if fp > 0:
            for i in range(10):
                v = 0.25 + 0.75 * abs(math.sin(i * 0.9 + 2) * math.cos(i * 0.37 + 2))
                hh = (16 + 230 * v) * (1 - 0.4 * fp)
                x = lerp(470 + i * 17, 1180 + i * 12, fp); y = lerp(520, 470, fp) - math.sin(math.pi * fp) * 160
                rrect(ctx, x, y - hh / 2, 10, hh, 5); src(ctx, C['yellow'], 1 - fp * 0.5); ctx.fill()
        pr = eback(prog(lt, l4 + 1.4, l4 + 1.8))
        if pr > 0:
            robot(ctx, 1450, 560, 1.15 * pr, 1.0 if lt > l4 + 2.3 else 0.0, t)
            if lt > l4 + 2.3:
                wave_bars(ctx, 1290, 840, 20, 16, 90, t, C['yellow'], seed=2, grow=prog(lt, l4 + 2.3, l4 + 2.8))
        source_line(ctx, 'e.g. Microsoft VALL-E (2023), Alibaba Qwen3-TTS (2025)', 1)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a4)


# ===================================================================== 3  THE HEIST
random.seed(21)
SKY = []
x = -20
while x < W + 40:
    w_ = random.uniform(80, 170); h_ = random.uniform(160, 520)
    SKY.append((x, w_, h_, random.random())); x += w_ + random.uniform(4, 18)
TILES = ['CFO', 'Finance', 'Legal', 'Ops', 'Manager', 'You']
TILE_BG = ['#2b3f9e', '#3b2a8f', '#1f5a8f', '#5a2a7a', '#2a4a7a', '#1f6a5a']


def skyline(ctx, base, t, a=1.0):
    for (x, w_, h_, r) in SKY:
        rrect(ctx, x, base - h_, w_, h_ + 40, 8); src(ctx, '#18245e' if r > 0.5 else '#1d2c6e', a); ctx.fill()
        rnd = random.Random(int(x))
        for wy in range(int(base - h_ + 24), int(base - 10), 34):
            for wx in range(int(x + 14), int(x + w_ - 20), 30):
                if rnd.random() < 0.38:
                    on = 0.55 + 0.45 * math.sin(t * 0.7 + wx * 0.13 + wy * 0.07)
                    ctx.rectangle(wx, wy, 14, 18); src(ctx, C['yellow'], 0.55 * on * a); ctx.fill()


def call_grid(ctx, lt, t, l2, l4, gx, gy, scale=1.0):
    tw, th = 400, 270
    gl = math.sin(math.pi * prog(lt, l4 - 0.1, l4 + 0.45))
    for i, name in enumerate(TILES):
        col, row = i % 3, i // 3
        x, y = gx + col * (tw + 24), gy + row * (th + 24)
        Lk = LOOKS[i] if i < 5 else LOOKS[0]
        talk = 1.0 if i == 0 and lt < l4 else 0.0

        def draw(c, x=x, y=y, Lk=Lk, i=i, name=name, talk=talk):
            rrect(c, x, y, tw, th, 26); src(c, TILE_BG[i]); c.fill()
            c.save(); rrect(c, x, y, tw, th, 26); c.clip()
            face(c, x + tw / 2, y + 140, 0.58, Lk, 1.0 if (t + i) % 3 < 0.1 else 0, 1.0 + 0.6 * math.sin(t * 18) * talk)
            c.restore()
            if talk:
                rrect(c, x, y, tw, th, 26); c.set_line_width(7); src(c, C['green']); c.stroke()
            font(c, 28); w_ = c.text_extents(name).x_advance + 30
            rrect(c, x + 16, y + th - 54, w_, 40, 14); c.set_source_rgba(0, 0, 0.1, 0.55); c.fill()
            rich(c, [(name, C['white'])], x + 16 + w_ / 2, y + th - 34, 28, pop=False, shadow=False)
        if i < 5:
            glitched(ctx, draw, x - 4, y - 4, tw + 8, th + 8, gl * 0.85, int(t * 30) + i)
            if lt > l4 + 0.2:
                ctx.save(); rrect(ctx, x, y, tw, th, 26); ctx.clip()
                wire(ctx, x + tw / 2, y + 140, 0.58, prog(lt, l4 + 0.2, l4 + 0.5) * 0.8, t + i * 0.3); ctx.restore()
                rrect(ctx, x, y, tw, th, 26); ctx.set_line_width(6); src(ctx, C['red'], prog(lt, l4 + 0.2, l4 + 0.4))
                ctx.stroke()
                pill(ctx, x + tw - 80, y + 40, 'FAKE', C['red'], C['white'], 30, prog(lt, l4 + 0.3 + i * 0.08, l4 + 0.55 + i * 0.08))
        else:
            draw(ctx)
            pill(ctx, x + tw - 80, y + 40, 'REAL', C['green'], C['dark'], 30, prog(lt, l4 + 0.9, l4 + 1.15))


def s3(ctx, lt, t, L):
    l0, l1, l2, l3, l4, l5 = [a for a, b in L]
    # ---- night city + worker (lines 0-1)
    if lt < l2 + 0.4:
        bg(ctx, t, top='#070c2c', bot='#1a1f5a', glow_col='#5a2a7a', gy=900, stars=0.8)
        zoom = 1 + 2.4 * ss(prog(lt, l1 + 1.2, l2 + 0.3)) ** 2
        ctx.save(); ctx.translate(1140, 560); ctx.scale(zoom, zoom); ctx.translate(-1140, -560)
        circle(ctx, 1650, 180, 70, '#f4f1d0'); glow(ctx, 1650, 180, 200, '#f4f1d0', 0.3)
        skyline(ctx, 760, t)
        rich(ctx, [('Hong Kong · early 2024', C['grey'])], 160, 120, 40, prog(lt, 0.3, 0.6), align='left', w='normal')
        # office floor
        rrect(ctx, 300, 760, 1320, 400, 30); src(ctx, '#232f7a'); ctx.fill()
        rrect(ctx, 700, 700, 900, 26, 13); src(ctx, '#4161d6'); ctx.fill()
        for lx in (740, 1540):
            ctx.rectangle(lx, 720, 18, 140); src(ctx, '#2c419b'); ctx.fill()
        person(ctx, 560, 900, 1.5, shirt='#3ee0ff', arm_l=0.2, arm_r=1.2 + 0.05 * math.sin(t * 30))
        laptop(ctx, 1140, 702, 2.1, t=t)
        if l1 + 0.2 < lt:
            rich(ctx, [('?', C['yellow'])], 560 + 6 * math.sin(t * 6), 520, 120, prog(lt, l1 + 0.2, l1 + 0.5))
        ctx.restore()
        # email notification
        pe = eback(prog(lt, l0 + 1.4, l0 + 1.9))
        if pe > 0 and zoom < 1.5:
            def mail():
                card(ctx, 1180, 230, 620, 210, '#f4f6ff', 28, stroke=False)
                rrect(ctx, 1210, 270, 90, 64, 10); src(ctx, C['orange']); ctx.fill()
                ctx.move_to(1210, 272); ctx.line_to(1255, 310); ctx.line_to(1300, 272); ctx.set_line_width(6)
                src(ctx, C['white']); ctx.stroke()
                rich(ctx, [('From: CFO', C['dark'])], 1330, 290, 36, pop=False, align='left', shadow=False)
                rich(ctx, [('"Confidential transaction"', '#6b7fb8')], 1330, 340, 30, pop=False, align='left',
                     shadow=False, w='normal')
                pill(ctx, 1700, 400, 'URGENT', C['red'], C['white'], 26, 1)
            pop_scale(ctx, 1490, 335, pe, mail)
        if zoom > 2.6:
            ctx.set_source_rgba(0.02, 0.03, 0.1, prog(zoom, 2.6, 3.4)); ctx.paint()
        if lt < l2 - 0.1: return
    # ---- video call (lines 2-4) + projection
    def rest():
        bg(ctx, t, glow_col='#7a2f5e', gy=560)
        if lt < l5 - 0.2:
            a = prog(lt, l2 - 0.1, l2 + 0.3)
            sx = 1 - 0.55 * ss(prog(lt, l3 - 0.2, l3 + 0.6)) * (1 - ss(prog(lt, l4 - 0.6, l4 - 0.1)))
            ctx.push_group()
            ctx.save(); ctx.translate(960, 520); ctx.scale(sx, sx); ctx.translate(-960, -520)
            card(ctx, 270, 150, 1380, 760, '#121a48', 40)
            for i, c in enumerate((C['red'], C['yellow'], C['green'])): circle(ctx, 320 + i * 34, 192, 10, c)
            rich(ctx, [('Video call · Confidential', C['grey'])], 960, 192, 30, pop=False, w='normal', shadow=False)
            call_grid(ctx, lt, t, l2, l4, 324, 236)
            ctx.restore()
            # transfers (line 3)
            if l3 < lt < l4 + 0.2:
                for k in range(15):
                    p = prog(lt, l3 + 0.5 + k * 0.17, l3 + 1.4 + k * 0.17)
                    if 0 < p < 1:
                        x = lerp(1180, 1820, eo(p)); y = lerp(520, 300 + 40 * (k % 5), eo(p)) - math.sin(math.pi * p) * 120
                        money(ctx, x, y, 1.0, rot=p * 2 + k, a=1 - 0.6 * p ** 4)
                n = int(clamp((lt - l3 - 0.5) / 0.17 + 1, 0, 15))
                v = 25_000_000 * ss(prog(lt, l3 + 0.5, l3 + 0.5 + 15 * 0.17 + 0.6))
                pa = prog(lt, l3 + 0.3, l3 + 0.6) * (1 - prog(lt, l4 - 0.6, l4 - 0.2))
                rich(ctx, [('$' + counter_text(v), C['green'])], 1520, 760, 96, pa)
                rich(ctx, [(f'transfer {max(1, n)} of 15', C['grey'])], 1520, 860, 44, pa, w='normal')
            ctx.pop_group_to_source(); ctx.paint_with_alpha(a * (1 - prog(lt, l5 - 0.6, l5 - 0.2)))
        if lt > L[4][1] - 0.6 and lt < l5:
            pass
        # ---- line 5: Deloitte projection
        if lt > l5 - 0.4:
            a5 = prog(lt, l5 - 0.3, l5 + 0.1)
            ctx.push_group()
            title(ctx, [('AI-powered fraud losses in the US', C['white'])], 150, 60, prog(lt, l5 + 0.3, l5 + 0.6))
            rich(ctx, [('(projection)', C['grey'])], 960, 220, 36, prog(lt, l5 + 0.5, l5 + 0.8), w='normal')
            base = 770
            bars = [(2023, 12.3, False), (2024, 16.2, True), (2025, 21.4, True), (2026, 28.3, True), (2027, 40.0, True)]
            for k, (yr, v, proj) in enumerate(bars):
                if k not in (0, 4): continue
                pass
            for k, (yr, v, proj) in enumerate([(2023, 12.3, False), (2027, 40.0, True)]):
                bx = 640 + k * 480
                hh = 470 * v / 40 * eo(prog(lt, l5 + 1.0 + k * 1.2, l5 + 2.2 + k * 1.2))
                rich(ctx, [(str(yr), C['white'])], bx + 90, base + 50, 44, prog(lt, l5 + 0.6, l5 + 0.9), pop=False)
                if hh > 1:
                    rrect(ctx, bx, base - hh, 180, hh, 22); src(ctx, C['orange'] if not proj else C['red'], 0.95 if not proj else 0.75)
                    ctx.fill()
                    if proj:
                        ctx.save(); rrect(ctx, bx, base - hh, 180, hh, 22); ctx.clip()
                        for s_ in range(-20, 40):
                            ctx.move_to(bx + s_ * 24, base); ctx.line_to(bx + s_ * 24 + 300, base - 300)
                        ctx.set_line_width(6); ctx.set_source_rgba(1, 1, 1, 0.12); ctx.stroke(); ctx.restore()
                    vv = v * eo(prog(lt, l5 + 1.0 + k * 1.2, l5 + 2.2 + k * 1.2))
                    rich(ctx, [(f'${vv:.1f}B' if k == 0 else f'${vv:.0f}B', C['white'])], bx + 90, base - hh - 50, 60, 1, pop=False)
            pa = prog(lt, l5 + 2.6, l5 + 3.1)
            if pa > 0:
                ctx.move_to(860, 600); ctx.curve_to(960, 480, 1000, 380, lerp(860, 1080, pa), lerp(600, 330, pa))
                ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND); src(ctx, C['yellow'], pa); ctx.stroke()
                rich(ctx, [('3x', C['yellow'])], 1010, 560, 70, prog(lt, l5 + 3.0, l5 + 3.3))
            source_line(ctx, 'Source: Deloitte Center for Financial Services, 2024', 1)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(a5)
        else:
            source_line(ctx, 'Source: CNN, May 2024 (Arup case)', prog(lt, l0 + 0.5, l0 + 1.0))

    if lt < l2 + 0.3:
        ctx.push_group(); rest(); ctx.pop_group_to_source(); ctx.paint_with_alpha(prog(lt, l2 - 0.1, l2 + 0.3))
    else:
        rest()
