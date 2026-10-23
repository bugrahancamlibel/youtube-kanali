from props_ai import *


def starts(L): return [a for a, b in L]


def fade_block(ctx, a, fn):
    if a <= 0: return
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)


def win(lt, a0, a1, f=0.25):
    """visibility window [a0, a1] with fades."""
    return prog(lt, a0 - f, a0 + f) * (1 - prog(lt, a1 - f, a1 + f))


JOBS = [('cashier', '#ff8a3d'), ('driver', '#3ee0ff'), ('doctor', '#5ee38a'), ('coder', '#b28cff'), ('lawyer', '#ffd23f'),
        ('CEO', '#ff4f81')]


# ===================================================================== 0  COLD OPEN
def s0(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    # ---- line 0: bedroom, no alarm
    def bedroom():
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#2a3f9e')); g.add_color_stop_rgba(1, *hexc('#5a3a8a'))
        ctx.set_source(g); ctx.paint()
        rrect(ctx, 1120, 120, 640, 520, 30); src(ctx, '#ffc98a'); ctx.fill()
        ctx.save(); rrect(ctx, 1120, 120, 640, 520, 30); ctx.clip()
        circle(ctx, 1500, 520, 120, '#fff0b0'); glow(ctx, 1500, 520, 300, '#ffd23f', 0.5)
        city(ctx, 640, t, 0.2, seed=3, x0=1100, x1=1780)
        for k in range(3):
            x = (1100 + ((t * 60 + k * 230) % 700))
            ctx.move_to(x, 260 + k * 40); ctx.line_to(x + 40, 260 + k * 40); ctx.set_line_width(6); src(ctx, C['cyan'], 0.8); ctx.stroke()
        ctx.restore()
        ctx.move_to(1440, 120); ctx.line_to(1440, 640); ctx.set_line_width(14); src(ctx, '#2a3f9e'); ctx.stroke()
        ctx.rectangle(0, 820, W, 260); src(ctx, '#3a2a6a'); ctx.fill()
        rrect(ctx, 160, 620, 760, 200, 30); src(ctx, '#f4f6ff'); ctx.fill()
        rrect(ctx, 160, 600, 220, 90, 40); src(ctx, '#d4dcf2'); ctx.fill()
        rrect(ctx, 300, 640, 640, 120, 50); src(ctx, '#4161d6'); ctx.fill()
        circle(ctx, 270, 610, 52, C['skin']); ctx.new_path(); ctx.arc(270, 600, 54, math.pi * 1.0, math.pi * 1.9); ctx.close_path()
        src(ctx, C['hair']); ctx.fill()
        ctx.move_to(250, 612); ctx.line_to(266, 612); ctx.move_to(278, 612); ctx.line_to(294, 612); ctx.set_line_width(4); src(ctx, C['dark']); ctx.stroke()
        for k in range(3):
            ph = (t * 0.5 + k / 3) % 1
            rich(ctx, [('z', C['white'])], 330 + 60 * ph + k * 10, 540 - 120 * ph, 30 + 20 * ph, 1 - ph, pop=False, shadow=False)
        rrect(ctx, 960, 700, 160, 120, 10); src(ctx, '#8c6a45'); ctx.fill()
        alarm_clock(ctx, 1040, 650, 1.0, t, ring=0)
        x_mark(ctx, 1040, 650, 50, prog(lt, l0 + 2.2, l0 + 2.6))
        pill(ctx, 300, 120, 'Monday · the near future', C['yellow'], C['dark'], 32, prog(lt, 0.3, 0.7))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), bedroom)
    # ---- line 1: AI everywhere
    def vignettes():
        bg(ctx, t, top='#0b1640', bot='#2a3a8a', glow_col='#3a5ab8', gy=700)
        items = [(l1 + 0.2, 'drives', C['cyan']), (l1 + 1.6, 'codes', C['pink']), (l1 + 2.6, 'reads X-rays', C['green']),
                 (l1 + 3.5, 'answers phones', C['yellow']), (l1 + 4.6, 'argues cases', C['orange'])]
        for k, (st, lab, col) in enumerate(items):
            p = eback(prog(lt, st, st + 0.4))
            if p <= 0: continue
            cx = 220 + k * 370; cy = 520
            ctx.save(); ctx.translate(cx, cy); ctx.scale(p, p); ctx.translate(-cx, -cy)
            card(ctx, cx - 165, 230, 330, 470, '#20307e', 36); glow(ctx, cx, 450, 200, col, 0.3)
            if k == 0:
                truck(ctx, cx + 10, 560, 0.62, t=t)
            else:
                bot(ctx, cx - 50, 640, 1.25, t=t, arm_r=1.2)
                if k == 1: laptop(ctx, cx + 70, 600, 0.6, t=t)
                if k == 2: xray(ctx, cx + 80, 470, 0.8)
                if k == 3: headset(ctx, cx - 50, 420, 0.55)
                if k == 4: gavel(ctx, cx + 80, 620, 0.6, ang=0.4 * math.sin(t * 6))
            ctx.restore()
            rich(ctx, [('AI ' + lab, col)], cx, 760, 38, p, pop=False, maxw=320)
    fade_block(ctx, win(lt, l1 - 0.2, l2), vignettes)
    # ---- line 2: humans replaced
    def replaced():
        bg(ctx, t, glow_col='#4a2a9a', gy=560)
        hills(ctx, 860, '#1d2c6e', amp=0)
        for k, (job, col) in enumerate(JOBS):
            x = 260 + k * 280
            sw = ss(prog(lt, l2 + 0.6 + k * 0.45, l2 + 1.1 + k * 0.45))
            person(ctx, x - 700 * sw ** 1.5, 860, 1.25, shirt=col, a=1 - sw)
            bot(ctx, x + 400 * (1 - sw), 860, 1.25, a=sw, t=t, arm_r=0.6)
            pill(ctx, x, 950, job, col, C['dark'], 30, prog(lt, l2 + 0.1, l2 + 0.4))
        rich(ctx, [('never sleeps · never asks for a raise', C['grey'])], 960, 200, 44, prog(lt, l2 + 3.4, l2 + 3.7), w='normal')
    fade_block(ctx, win(lt, l2 - 0.2, l3), replaced)
    # ---- line 3: paradise or disaster -> title
    def split():
        ctx.save(); ctx.rectangle(0, 0, W / 2, H); ctx.clip()
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#3ee0ff')); g.add_color_stop_rgba(1, *hexc('#ffd28a'))
        ctx.set_source(g); ctx.paint()
        circle(ctx, 300, 220, 80, '#fff3b0'); hills(ctx, 820, '#f4d28a', amp=20)
        ctx.move_to(250, 820); ctx.curve_to(240, 600, 260, 450, 300, 380); ctx.set_line_width(22); src(ctx, '#8c6a45'); ctx.stroke()
        for k in range(5):
            a_ = -2.6 + k * 0.5
            ctx.move_to(300, 380); ctx.curve_to(300 + 90 * math.cos(a_), 380 + 60 * math.sin(a_), 300 + 160 * math.cos(a_), 380 + 120 * math.sin(a_) + 40,
                                                300 + 180 * math.cos(a_), 380 + 150 * math.sin(a_) + 60)
            ctx.set_line_width(26); src(ctx, '#2f8f58'); ctx.stroke()
        ctx.move_to(420, 690); ctx.curve_to(520, 760, 700, 760, 800, 690); ctx.set_line_width(10); src(ctx, '#ff8a3d'); ctx.stroke()
        person(ctx, 610, 760, 0.9, shirt=C['orange'], arm_l=2.6, arm_r=2.6, rot=1.45)
        rich(ctx, [('PARADISE?', C['dark'])], 480, 130, 80, prog(lt, l3 + 0.2, l3 + 0.5), shadow=False)
        ctx.restore()
        ctx.save(); ctx.rectangle(W / 2, 0, W / 2, H); ctx.clip()
        bg(ctx, t, top='#1a0f2a', bot='#3a1a2a', glow_col='#7a1a2a', gx=1440, gy=600)
        city(ctx, 800, t, 0.15, seed=21, x0=960, x1=W)
        for k in range(5):
            person(ctx, 1080 + k * 150, 900, 0.9, shirt='#5a5f7a', arm_l=0.2, arm_r=0.2 + 2.2 * (k % 2))
        rich(ctx, [('DISASTER?', C['red'])], 1440, 130, 80, prog(lt, l3 + 1.3, l3 + 1.6))
        ctx.restore()
        ctx.move_to(W / 2, 0); ctx.line_to(W / 2, H); ctx.set_line_width(8); src(ctx, C['white'], 0.8); ctx.stroke()
    te = L[3][1]
    fade_block(ctx, win(lt, l3 - 0.2, te + 0.3), split)
    def ttl():
        bg(ctx, t, glow_col='#4a2a9a', gy=560)
        bot(ctx, 1520, 900, 2.4, t=t, arm_l=0.3, arm_r=0.3)
        person(ctx, 400, 900, 2.4, shirt=C['orange'], arm_l=0.3, arm_r=0.3)
        rich(ctx, [('WHAT IF', C['white'])], 960, 330, 100, prog(lt, te + 0.2, te + 0.5))
        rich(ctx, [('AI TOOK', C['cyan'])], 960, 480, 150, prog(lt, te + 0.35, te + 0.65))
        rich(ctx, [('ALL THE JOBS?', C['yellow'])], 960, 640, 130, prog(lt, te + 0.5, te + 0.8))
    fade_block(ctx, prog(lt, te + 0.1, te + 0.5), ttl)


# ===================================================================== 1  ALREADY STARTING
def s1(ctx, lt, t, L):
    l0, l1 = starts(L)
    bg(ctx, t, glow_col='#26408f', gy=560)

    def news():
        pc = eback(prog(lt, l0 + 0.6, l0 + 1.0))
        def paper():
            card(ctx, 360, 200, 1200, 560, '#f4f1e8', 20, stroke=False)
            rrect(ctx, 360, 200, 1200, 90, 20); src(ctx, C['red']); ctx.fill()
            rich(ctx, [('BREAKING NEWS', C['white'])], 520, 246, 44, pop=False, shadow=False, align='left')
            rich(ctx, [('22 October 2026', '#ffe0e0')], 1330, 246, 30, pop=False, shadow=False, w='normal')
            rich(ctx, [('Barclays to cut', C['dark'])], 960, 380, 84, pop=False, shadow=False)
            rich(ctx, [('5,000 jobs', C['red'])], 960, 490, 110, pop=False, shadow=False)
            rich(ctx, [('"...technology change efficiency, driven by AI"', '#6b7fb8')], 960, 600, 36, pop=False, shadow=False, w='normal')
            for i, wl in enumerate((900, 820, 600)):
                rrect(ctx, 510, 650 + i * 30, wl, 14, 7); src(ctx, '#d8d2c0'); ctx.fill()
        ctx.save(); ctx.translate(960, 480); ctx.rotate(-0.03 * (1 - pc)); ctx.translate(-960, -480)
        pop_scale(ctx, 960, 480, pc, paper); ctx.restore()
        source_line(ctx, 'Source: Barclays Q3 2026 results, via iHeart / Bloomberg', 1)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), news)

    def chart():
        title(ctx, [('Workers aged 22–25 in AI-exposed jobs', C['white'])], 140, 54, prog(lt, l1 + 0.3, l1 + 0.6))
        x0, x1, y0 = 320, 1500, 760
        ctx.move_to(x0, 260); ctx.line_to(x0, y0); ctx.line_to(x1 + 40, y0); ctx.set_line_width(5); src(ctx, C['grey']); ctx.stroke()
        p = prog(lt, l1 + 1.4, l1 + 4.5)
        for k, (col, drop, lab) in enumerate(((C['green'], 0.02, 'other jobs'), (C['red'], 0.13, 'AI-exposed jobs'))):
            ctx.new_path()
            for i in range(61):
                u = i / 60
                if u > p: break
                yy = 420 + 300 * (drop * ss((u - 0.4) / 0.6) * 4 if u > 0.4 else 0) * (1 if k else -0.5)
                (ctx.move_to if i == 0 else ctx.line_to)(lerp(x0, x1, u), yy)
            ctx.set_line_width(10); src(ctx, col); ctx.stroke()
            if p >= 1:
                yy = 420 + 300 * drop * 4 * (1 if k else -0.5)
                rich(ctx, [(lab, col)], x1 + 30, yy, 34, 1, pop=False, align='left')
        rich(ctx, [('-13%', C['red'])], 1250, 640, 96, prog(lt, l1 + 4.3, l1 + 4.6))
        for k, (fn, lab) in enumerate(((headset, 'customer service'), (None, 'coding'))):
            x = 500 + k * 300; y = 870
            pp = prog(lt, l1 + 2.6 + k * 0.6, l1 + 2.9 + k * 0.6)
            if pp > 0:
                circle(ctx, x, y, 50 * pp, '#20307e')
                if fn: fn(ctx, x, y - 10, 0.6 * pp)
                else: rich(ctx, [('</>', C['white'])], x, y, 36 * pp, 1, pop=False)
                rich(ctx, [(lab, C['white'])], x, y + 80, 30, pp, pop=False)
        rich(ctx, [('2021', C['grey'])], x0, y0 + 40, 28, 1, pop=False, w='normal')
        rich(ctx, [('2025', C['grey'])], x1, y0 + 40, 28, 1, pop=False, w='normal')
        source_line(ctx, 'Source: Brynjolfsson, Chandar & Chen, Stanford Digital Economy Lab, 2025 (illustrative curve)', 1)
    fade_block(ctx, prog(lt, l1 - 0.2, l1 + 0.3), chart)


# ===================================================================== 2  WE'VE BEEN HERE BEFORE
def s2(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)

    def farm():
        sep = 1 - prog(lt, l0 + 3.5, l0 + 4.5)
        bg(ctx, t, top=lerp_col('#2a3a8a', '#6a4a3a', sep), bot=lerp_col('#3a4a9a', '#a07a4a', sep), glow_col='#ffb34a', gy=700, stars=0.2)
        hills(ctx, 800, lerp_col('#2f6a3a', '#7a6a3a', sep), amp=30)
        rich(ctx, [('1900' if sep > 0.5 else 'TODAY', C['yellow'])], 960, 140, 90, prog(lt, 0.3, 0.6), pop=False)
        if sep > 0.02:
            for k in range(10):
                x = 330 + k * 140; farmer = k < 4
                person(ctx, x, 760, 1.0, shirt='#c98a3a' if farmer else '#5a6ab8', a=sep)
                if farmer:
                    ctx.save(); ctx.translate(x, 760 - 230); ctx.scale(1, 0.3); circle(ctx, 0, 0, 55, '#e8c060', sep); ctx.restore()
            rich(ctx, [('~4 in 10', C['white'])], 960, 900, 70, prog(lt, l0 + 1.2, l0 + 1.5) * sep)
            rich(ctx, [('workers on farms', C['grey'])], 960, 970, 36, prog(lt, l0 + 1.4, l0 + 1.7) * sep, w='normal')
        if sep < 0.98:
            for k in range(100):
                r_, c_ = divmod(k, 20)
                x = 390 + c_ * 60; y = 340 + r_ * 90
                circle(ctx, x, y, 18, C['yellow'] if k < 2 else '#5a6ab8', 1 - sep)
            rich(ctx, [('fewer than 2 in 100', C['yellow'])], 960, 900, 70, prog(lt, l0 + 4.6, l0 + 4.9))
        source_line(ctx, 'Source: USDA / Historical Statistics of the US', 1)
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), farm)

    def luddites():
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *hexc('#3a2a4a')); g.add_color_stop_rgba(1, *hexc('#5a3a3a'))
        ctx.set_source(g); ctx.paint()
        ctx.rectangle(0, 820, W, 260); src(ctx, '#2a1f3a'); ctx.fill()
        broken = prog(lt, l1 + 1.8, l1 + 2.2)
        loom(ctx, 1100, 820, 1.6, t, broken)
        sw = math.sin(t * 6) if lt < l1 + 2.2 else 0
        person(ctx, 640, 820, 1.7, shirt='#7a4a3a', arm_r=2.4 + 0.6 * sw, arm_l=0.3)
        gavel(ctx, 640 + 40, 820 - 1.7 * 136 - 60, 0.9, ang=-0.6 + 0.9 * (sw + 1) / 2)
        if 0 < broken < 1 or (l1 + 1.8 < lt < l1 + 2.6):
            spark(ctx, 1000, 560, 100, t, 1, col=C['orange'])
        pill(ctx, 300, 120, 'England · 1811', C['yellow'], C['dark'], 34, prog(lt, l1 + 0.2, l1 + 0.5))
        rich(ctx, [('The Luddites', C['white'])], 960, 160, 70, prog(lt, l1 + 0.6, l1 + 0.9))
    fade_block(ctx, win(lt, l1 - 0.2, l2), luddites)

    def atms():
        bg(ctx, t, glow_col='#1f5a8f', gy=700)
        hills(ctx, 860, '#1d2c6e', amp=0)
        pa = eback(prog(lt, l2 + 0.3, l2 + 0.7))
        if pa > 0:
            ctx.save(); ctx.translate(380, 860); ctx.scale(pa, pa); ctx.translate(-380, -860); atm(ctx, 380, 860, 1.3); ctx.restore()
        tq = prog(lt, l2 + 1.2, l2 + 1.6)
        person(ctx, 700, 860, 1.2, shirt=C['green'], a=tq)
        pill(ctx, 700, 520, 'teller', C['green'], C['dark'], 30, tq)
        rich(ctx, [('?', C['yellow'])], 760, 470, 70, tq * (1 - prog(lt, l2 + 3.2, l2 + 3.4)))
        for k in range(4):
            p = eback(prog(lt, l2 + 3.0 + k * 0.4, l2 + 3.3 + k * 0.4))
            if p > 0:
                x = 1000 + k * 240
                ctx.save(); ctx.translate(x, 860); ctx.scale(p * 0.85, p * 0.85); ctx.translate(-x, -860); bank(ctx, x, 860, 1.0)
                ctx.restore()
                person(ctx, x, 940, 0.5, shirt=C['green'], a=p)
        rich(ctx, [('more branches', C['white'])], 1360, 380, 54, prog(lt, l2 + 3.6, l2 + 3.9))
        source_line(ctx, 'Source: James Bessen (via Conversable Economist, 2015)', 1)
    fade_block(ctx, win(lt, l2 - 0.2, l3), atms)

    def newjobs():
        bg(ctx, t, glow_col='#4a2a9a', gy=560)
        jobs = [('app developer', C['cyan']), ('YouTuber', C['red']), ('drone pilot', C['yellow']), ('data scientist', C['green']),
                ('game designer', C['pink']), ('cybersecurity', C['orange'])]
        for k, (lab, col) in enumerate(jobs):
            p = eback(prog(lt, l3 + 0.3 + k * 0.3, l3 + 0.6 + k * 0.3))
            if p <= 0: continue
            ang = -math.pi / 2 + k * math.pi / 3 + 0.2 * math.sin(t * 0.5)
            x = 960 + 520 * math.cos(ang); y = 540 + 300 * math.sin(ang)
            person(ctx, x, y + 80, 0.7 * p, shirt=col)
            pill(ctx, x, y + 120, lab, col, C['dark'], 28, p)
        n = int(60 * eo(prog(lt, l3 + 2.4, l3 + 3.4)))
        rich(ctx, [(f'{n}%', C['cyan'])], 960, 500, 160, prog(lt, l3 + 2.3, l3 + 2.6))
        rich(ctx, [("of 2018's jobs didn't exist in 1940", C['white'])], 960, 620, 40, prog(lt, l3 + 2.8, l3 + 3.1))
        source_line(ctx, 'Source: Autor et al., Quarterly Journal of Economics, 2024', 1)
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), newjobs)


# ===================================================================== 3  THIS TIME IS DIFFERENT
def s3(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, glow_col='#3a2a8a', gy=560)

    def mb():
        pm = eback(prog(lt, l0 + 1.0, l0 + 1.4)); pb = eback(prog(lt, l0 + 2.8, l0 + 3.2))
        if pm > 0:
            ctx.save(); ctx.translate(560, 500); ctx.scale(pm, pm); ctx.rotate(-0.3 + 0.15 * math.sin(t * 3))
            rrect(ctx, -220, -14, 440, 28, 14); src(ctx, '#d4dcf2'); ctx.fill()
            for sx in (-1, 1):
                rrect(ctx, sx * 170 - 30, -110, 60, 220, 18); src(ctx, '#5a6ab8'); ctx.fill()
                rrect(ctx, sx * 230 - 22, -80, 44, 160, 14); src(ctx, '#3a4a9a'); ctx.fill()
            ctx.restore()
            rich(ctx, [('old machines: muscles', C['white'])], 560, 760, 46, pm, pop=False)
        if pb > 0:
            glow(ctx, 1360, 500, 260, C['pink'], 0.5 * pb)
            brain(ctx, 1360, 500, 1.6 * pb, t=t)
            rich(ctx, [('AI: brains', C['pink'])], 1360, 760, 56, pb, pop=False)
        rich(ctx, [('vs', C['grey'])], 960, 500, 70, prog(lt, l0 + 2.4, l0 + 2.6))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), mb)

    def imf():
        earth(ctx, 700, 540, 250, t)
        p = prog(lt, l1 + 1.0, l1 + 2.4)
        for k, (cx, frac, lab, col, st) in enumerate(((700, 0.40, 'worldwide', C['cyan'], 1.0), (1380, 0.60, 'rich countries', C['pink'], 4.2))):
            pp = prog(lt, l1 + st, l1 + st + 1.4)
            if pp <= 0: continue
            r = 300 if k == 0 else 200
            cy = 540
            ctx.new_path(); ctx.arc(cx, cy, r, 0, 2 * math.pi); ctx.set_line_width(36); ctx.set_source_rgba(1, 1, 1, 0.1); ctx.stroke()
            ctx.new_path(); ctx.arc(cx, cy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac * pp); ctx.set_line_width(36)
            src(ctx, col); ctx.stroke()
            if k == 1:
                rich(ctx, [(f'{int(60 * pp)}%', C['white'])], cx, cy, 110, 1, pop=False)
            else:
                rich(ctx, [(f'~{int(40 * pp)}%', C['white'])], cx, cy + 360, 80, 1, pop=False)
            rich(ctx, [(lab, col)], cx, cy + (430 if k == 0 else 260), 40, pp, pop=False, w='normal')
        rich(ctx, [('of jobs exposed to AI', C['white'])], 960, 110, 56, prog(lt, l1 + 1.4, l1 + 1.7))
        source_line(ctx, 'Source: IMF, "Gen-AI: Artificial Intelligence and the Future of Work", Jan 2024', 1)
    fade_block(ctx, win(lt, l1 - 0.2, l2), imf)

    def exposed():
        items = [('lawyer', lambda x, y: gavel(ctx, x + 10, y + 70, 0.55)), ('accountant', lambda x, y: calc(ctx, x, y, 1.1)),
                 ('programmer', lambda x, y: rich(ctx, [('</>', C['white'])], x, y, 64, 1, pop=False)),
                 ('writer', lambda x, y: pen(ctx, x, y, 1.0))]
        for k, (lab, fn) in enumerate(items):
            p = eback(prog(lt, l2 + 0.1 + k * 0.45, l2 + 0.45 + k * 0.45))
            if p <= 0: continue
            x = 330 + k * 420; y = 460
            ctx.save(); ctx.translate(x, y); ctx.scale(p, p); ctx.translate(-x, -y)
            card(ctx, x - 160, y - 200, 320, 400, '#20307e', 36)
            pulse = prog(lt, l2 + 2.6, l2 + 3.0)
            if pulse > 0: glow(ctx, x, y, 260, C['red'], 0.4 * pulse * (0.7 + 0.3 * math.sin(t * 6 + k)))
            circle(ctx, x, y - 40, 90, '#2f4aa8'); fn(x, y - 40)
            rich(ctx, [(lab, C['white'])], x, y + 120, 40, 1, pop=False)
            ctx.restore()
            pill(ctx, x, y - 200, 'EXPOSED', C['red'], C['white'], 28, prog(lt, l2 + 2.8 + k * 0.1, l2 + 3.1 + k * 0.1))
        rich(ctx, [('the "safe" jobs', C['yellow'])], 960, 110, 56, prog(lt, l2 + 1.6, l2 + 1.9))
    fade_block(ctx, win(lt, l2 - 0.2, l3), exposed)

    def halves():
        sp = ss(prog(lt, l3 + 0.4, l3 + 1.4))
        for k in range(20):
            r_, c_ = divmod(k, 5)
            left = k % 2 == 0
            x = 960 + (-1 if left else 1) * (120 + c_ * 110) * (0.2 + 0.8 * sp) + (0 if sp > 0 else 0)
            y = 330 + r_ * 150
            if left:
                person(ctx, x, y + 90, 0.55, shirt=C['green'])
                if sp > 0.8:
                    ctx.move_to(x + 34, y - 80); ctx.line_to(x + 50, y - 56); ctx.line_to(x + 18, y - 56); ctx.close_path(); src(ctx, C['green']); ctx.fill()
            else:
                fade = 1 - 0.75 * prog(lt, l3 + 1.8, l3 + 3.0)
                person(ctx, x, y + 90, 0.55, shirt='#9aaad6', a=fade)
        rich(ctx, [('could benefit', C['green'])], 480, 960, 50, prog(lt, l3 + 1.0, l3 + 1.3))
        rich(ctx, [('could shrink or vanish', C['red'])], 1440, 960, 50, prog(lt, l3 + 2.0, l3 + 2.3))
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), halves)


# ===================================================================== 4  THE EXTREME
def s4(ctx, lt, t, L):
    l0, l1, l2, l3 = starts(L)
    bg(ctx, t, top='#0b1240', bot='#1f2a6a', glow_col='#3a2a8a', gy=600)

    def factory():
        rrect(ctx, 140, 700, 1640, 40, 20); src(ctx, '#3a4a9a'); ctx.fill()
        for k in range(16):
            ctx.new_path(); ctx.arc(200 + k * 102, 720, 16, 0, 2 * math.pi); src(ctx, '#5a6ab8'); ctx.fill()
        speed = 1 + 3 * prog(lt, l1, l1 + 2)
        for k in range(14):
            x = (k * 130 + (lt * 120 * speed)) % 1700 + 120
            box(ctx, x, 700, 1.1)
        for k in range(4):
            bot(ctx, 340 + k * 400, 690, 1.0, t=t, arm_r=1.0 + 0.4 * math.sin(t * 8 + k), arm_l=0.8 + 0.4 * math.cos(t * 8 + k))
        rich(ctx, [('AI does everything', C['white'])], 960, 150, 70, prog(lt, l0 + 0.4, l0 + 0.7))
        if lt > l1:
            n = int(1000 * (1 + 9 * prog(lt, l1 + 0.4, l1 + 2.4)))
            rich(ctx, [(f'output: {n:,}/hr', C['green'])], 560, 300, 50, prog(lt, l1 + 0.3, l1 + 0.6), pop=False)
            price = 100 * (1 - 0.95 * prog(lt, l1 + 0.4, l1 + 2.4))
            rich(ctx, [(f'price: ${price:.0f}', C['yellow'])], 1360, 300, 50, prog(lt, l1 + 0.3, l1 + 0.6), pop=False)
            pe = eback(prog(lt, l1 + 3.4, l1 + 3.8))
            if pe > 0:
                ctx.set_source_rgba(0.02, 0.03, 0.12, 0.6 * pe); ctx.paint()
                person(ctx, 820, 900, 1.6, shirt=C['orange'], arm_r=1.2)
                envelope(ctx, 1020, 620, 1.6 * pe)
                rich(ctx, [('wages', C['green'])], 1020, 500, 56, pe)
    fade_block(ctx, 1 - prog(lt, l2 - 0.2, l2 + 0.3), factory)

    def loop():
        # circular flow
        cx, cy = 960, 540
        comp = (560, 540); ppl = (1360, 540)
        rrect(ctx, comp[0] - 150, comp[1] - 110, 300, 220, 30); src(ctx, '#2f4aa8'); ctx.fill()
        rich(ctx, [('companies', C['white'])], comp[0], comp[1] + 150, 40, 1, pop=False)
        for k in range(3): bot(ctx, comp[0] - 70 + k * 70, comp[1] + 80, 0.55, t=t)
        for k in range(3): person(ctx, ppl[0] - 70 + k * 70, ppl[1] + 80, 0.55, shirt=[C['orange'], C['cyan'], C['pink']][k])
        rich(ctx, [('people', C['white'])], ppl[0], ppl[1] + 150, 40, 1, pop=False)
        brk = prog(lt, l2 + 0.6, l2 + 1.0)
        # top arrow: products
        ctx.new_path(); ctx.arc(cx, cy + 260, 480, math.pi * 1.25, math.pi * 1.75); ctx.set_line_width(10); src(ctx, C['yellow']); ctx.stroke()
        rich(ctx, [('products', C['yellow'])], cx, 230, 38, 1, pop=False)
        # bottom arrow: money (breaks)
        ctx.new_path(); ctx.arc(cx, cy - 260, 480, math.pi * 0.25, math.pi * 0.25 + math.pi * 0.5 * (1 - 0.5 * brk))
        ctx.set_line_width(10); src(ctx, C['green'], 1 - 0.6 * brk); ctx.stroke()
        rich(ctx, [('money', C['green'])], cx, 860, 38, 1 - brk, pop=False)
        if brk > 0:
            x_mark(ctx, cx, 780, 40, brk)
            rich(ctx, [('no wages... who buys?', C['red'])], cx, 860, 44, prog(lt, l2 + 1.2, l2 + 1.5))
        po = eback(prog(lt, l2 + 3.4, l2 + 3.8))
        if po > 0:
            top_hat_owner(ctx, 960, 520, 1.3 * po)
            for k in range(14):
                u = (t * 0.6 + k / 14) % 1
                coin(ctx, lerp(560, 960, u), 380 - math.sin(math.pi * u) * 120, 16, po)
            rich(ctx, [('owners of the machines', C['yellow'])], 960, 150, 48, po)
    fade_block(ctx, win(lt, l2 - 0.2, l3), loop)

    def robotax():
        bot(ctx, 760, 860, 2.0, t=t, arm_r=1.0)
        pf = eback(prog(lt, l3 + 0.5, l3 + 0.9))
        if pf > 0:
            def form():
                card(ctx, 1000, 300, 420, 520, '#f4f6ff', 20, stroke=False)
                rich(ctx, [('TAX FORM', C['dark'])], 1210, 360, 44, pop=False, shadow=False)
                for i in range(6): rrect(ctx, 1040, 420 + i * 50, 340 - (i % 3) * 60, 16, 8); src(ctx, '#c9d2f0'); ctx.fill()
            pop_scale(ctx, 1210, 560, pf, form)
            stamp(ctx, 1210, 660, 'ROBOT', C['red'], prog(lt, l3 + 1.4, l3 + 1.6), size=70)
        rich(ctx, [('"Tax the robots"', C['yellow'])], 960, 160, 70, prog(lt, l3 + 2.8, l3 + 3.1))
        rich(ctx, [('— idea floated by Bill Gates, 2017', C['grey'])], 960, 240, 36, prog(lt, l3 + 3.2, l3 + 3.5), w='normal')
    fade_block(ctx, prog(lt, l3 - 0.2, l3 + 0.3), robotax)


# ===================================================================== 5  BASIC INCOME
def s5(ctx, lt, t, L):
    l0, l1, l2 = starts(L)

    def ubi():
        bg(ctx, t, top='#0b1640', bot='#2a3a8a', glow_col='#3a5ab8', gy=700, stars=0.5)
        hills(ctx, 760, '#2a4a9a', amp=30, phase=0.6); hills(ctx, 880, '#1f357a', amp=24, phase=2.0)
        rnd = random.Random(7)
        hs = [(120 + k * 150 + rnd.uniform(-20, 20), 880 + rnd.uniform(-10, 20)) for k in range(12)]
        for x, y in hs: house(ctx, x, y, 0.9, rnd.choice(['#ff8a3d', '#ffd23f', '#3ee0ff', '#ff4f81', '#5ee38a']))
        for k, (x, y) in enumerate(hs):
            p = prog(lt, l0 + 1.4 + k * 0.12, l0 + 2.4 + k * 0.12)
            if 0 < p < 1:
                envelope(ctx, lerp(960, x, eo(p)), lerp(140, y - 120, eo(p)) - math.sin(math.pi * p) * 80, 0.8)
            elif p >= 1:
                circle(ctx, x, y - 130, 10, C['green'])
        rich(ctx, [('Universal Basic Income', C['white'])], 960, 150, 74, prog(lt, l0 + 0.4, l0 + 0.7))
        rich(ctx, [('to everyone · no strings attached', C['grey'])], 960, 240, 40, prog(lt, l0 + 2.6, l0 + 2.9), w='normal')
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), ubi)

    def study():
        bg(ctx, t, glow_col='#26408f', gy=560)
        title(ctx, [('$1,000 a month · 3 years · 1,000 people', C['white'])], 120, 54, prog(lt, l1 + 0.3, l1 + 0.6))
        for k in range(36):
            p = prog(lt, l1 + 0.8 + k * 0.05, l1 + 1.0 + k * 0.05)
            x = 220 + (k % 12) * 62; y = 260 + (k // 12) * 70
            rrect(ctx, x, y, 52, 56, 8); src(ctx, C['green'] if p > 0.5 else '#2a3a7a'); ctx.fill()
            if p > 0.5: rich(ctx, [('$', C['dark'])], x + 26, y + 30, 26, 1, pop=False, shadow=False)
        rich(ctx, [('36 payments', C['grey'])], 590, 520, 34, prog(lt, l1 + 2.6, l1 + 2.9), w='normal')
        # work hours bars
        pw = prog(lt, l1 + 4.0, l1 + 5.2)
        for k, (lab, v, col) in enumerate((('without', 1.0, '#9aaad6'), ('with cash', 0.965, C['cyan']))):
            y = 650 + k * 110
            rich(ctx, [(lab, C['white'])], 240, y + 30, 32, pw, pop=False, align='left', w='normal')
            rrect(ctx, 460, y, 560 * v * eo(pw), 60, 16); src(ctx, col); ctx.fill()
        rich(ctx, [('~1 hour/week less work', C['cyan'])], 760, 900, 44, prog(lt, l1 + 5.0, l1 + 5.3))
        # spending
        ps = prog(lt, l1 + 6.6, l1 + 8.0)
        cats = [('food', 0.34, C['orange']), ('rent', 0.33, C['pink']), ('transport', 0.33, C['yellow'])]
        a0 = -math.pi / 2
        for lab, f, col in cats:
            a1 = a0 + 2 * math.pi * f * ps
            ctx.move_to(1480, 560); ctx.arc(1480, 560, 220, a0, a1); ctx.close_path(); src(ctx, col); ctx.fill()
            mid = (a0 + a1) / 2
            if ps > 0.9: rich(ctx, [(lab, C['dark'])], 1480 + 130 * math.cos(mid), 560 + 130 * math.sin(mid), 34, 1, pop=False, shadow=False)
            a0 += 2 * math.pi * f
        rich(ctx, [('spent mostly on basics', C['white'])], 1480, 840, 40, prog(lt, l1 + 7.6, l1 + 7.9))
        source_line(ctx, 'Source: OpenResearch Unconditional Cash Study (via J-PAL, 2024)', 1)
    fade_block(ctx, win(lt, l1 - 0.2, l2), study)

    def alaska():
        bg(ctx, t, top='#0b1640', bot='#3a4a9a', glow_col='#5ee38a', gy=200, stars=0.8)
        aurora(ctx, 0, W, 40, 360, t, 0.5)
        ctx.new_path(); ctx.move_to(0, 760)
        for x, y in ((240, 520), (480, 700), (760, 480), (1060, 690), (1360, 500), (1640, 680), (1920, 560)): ctx.line_to(x, y)
        ctx.line_to(W, 1080); ctx.line_to(0, 1080); ctx.close_path(); src(ctx, '#e8ecff'); ctx.fill()
        ctx.rectangle(0, 860, W, 220); src(ctx, '#c9d2f0'); ctx.fill()
        mor = prog(lt, l2 + 4.6, l2 + 5.4)
        if mor < 1: derrick(ctx, 520, 860, 1.2, a=1 - mor)
        if mor > 0: server(ctx, 520, 860, 1.2, a=mor, t=t)
        rnd = random.Random(3)
        for k in range(6):
            x = 900 + k * 160; house(ctx, x, 900, 0.8, rnd.choice(['#ff8a3d', '#ffd23f', '#3ee0ff', '#ff4f81']))
            for j in range(2):
                u = (t * 0.4 + k * 0.15 + j * 0.5) % 1
                coin(ctx, lerp(560, x, u), 600 - math.sin(math.pi * u) * 180, 14, prog(lt, l2 + 1.0, l2 + 1.4))
        pill(ctx, 300, 120, 'Alaska · since 1982', C['yellow'], C['dark'], 34, prog(lt, l2 + 0.3, l2 + 0.6))
        rich(ctx, [('oil', C['white'])], 520, 980, 44, 1 - mor, pop=False)
        rich(ctx, [('computing power?', C['cyan'])], 520, 980, 44, mor, pop=False)
        source_line(ctx, 'Alaska Permanent Fund Dividend', 1)
    fade_block(ctx, prog(lt, l2 - 0.2, l2 + 0.3), alaska)


# ===================================================================== 6  MEANING
def s6(ctx, lt, t, L):
    l0, l1 = starts(L)
    bg(ctx, t, top='#1a2a6e', bot='#4a3a8a', glow_col='#ff8a5a', gy=800)

    def purpose():
        rrect(ctx, 300, 640, 1320, 30, 14); src(ctx, '#8c6a45'); ctx.fill()
        for k, col in enumerate((C['orange'], C['cyan'], C['pink'], C['green'])):
            x = 450 + k * 340
            person(ctx, x, 820, 1.3, shirt=col, arm_l=0.3 + 0.3 * math.sin(t * 3 + k), arm_r=0.5)
            laptop(ctx, x + 110, 640, 0.6, t=t)
        for k, (lab, col) in enumerate((('structure', C['yellow']), ('friends', C['cyan']), ('purpose', C['pink']))):
            p = eback(prog(lt, l0 + 1.6 + k * 0.7, l0 + 1.9 + k * 0.7))
            x = 520 + k * 440
            if p > 0:
                heart(ctx, x, 280, 1.2 * p, col) if k == 2 else circle(ctx, x, 280, 60 * p, col)
                rich(ctx, [(lab, C['white'])], x, 400, 46, p, pop=False)
        rich(ctx, [('more than money', C['yellow'])], 960, 110, 64, prog(lt, l0 + 0.4, l0 + 0.7))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), purpose)

    def keynes():
        pill(ctx, 360, 120, 'John Maynard Keynes · 1930', C['yellow'], C['dark'], 34, prog(lt, l1 + 0.3, l1 + 0.6))
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        for k, d in enumerate(days):
            x = 360 + k * 300
            rich(ctx, [(d, C['white'])], x + 110, 280, 34, 1, pop=False)
            pred = prog(lt, l1 + 1.6, l1 + 2.6)
            rrect(ctx, x, 320, 220, 180 * pred, 14); src(ctx, C['cyan']); ctx.fill()
            real = prog(lt, l1 + 4.6, l1 + 6.0)
            rrect(ctx, x, 560, 220, 380 * real, 14); src(ctx, C['orange']); ctx.fill()
        rich(ctx, [('predicted: 15 hours a week', C['cyan'])], 960, 530, 40, prog(lt, l1 + 2.4, l1 + 2.7), pop=False)
        rich(ctx, [('reality: we kept working', C['orange'])], 960, 1000, 44, prog(lt, l1 + 5.6, l1 + 5.9))
    fade_block(ctx, prog(lt, l1 - 0.2, l1 + 0.3), keynes)


# ===================================================================== 7  WHAT STAYS HUMAN
def s7(ctx, lt, t, L):
    l0, l1, l2, l3, l4 = starts(L)
    sun_ = ss(prog(lt, l4 - 0.4, l4 + 1.5))
    bg(ctx, t, top=lerp_col('#0b1640', '#2a2a7a', sun_), bot=lerp_col('#1c2d72', '#ff8a5a', sun_), glow_col=lerp_col('#35237e', '#ffd23f', sun_),
       gy=lerp(560, 820, sun_))

    def chess97():
        chessboard(ctx, 960, 600, 1.2)
        monitor(ctx, 960, 350, 1.0, screen='#1b2a6e')
        rich(ctx, [('CHECKMATE', C['green'])], 960, 250, 28, prog(lt, l0 + 3.0, l0 + 3.3), pop=False, shadow=False)
        person(ctx, 520, 900, 1.6, shirt='#3a3f6a', arm_l=0.2, arm_r=1.0 - 0.9 * prog(lt, l0 + 3.0, l0 + 3.5))
        pill(ctx, 300, 120, '1997', C['yellow'], C['dark'], 40, prog(lt, l0 + 1.8, l0 + 2.1))
    fade_block(ctx, 1 - prog(lt, l1 - 0.2, l1 + 0.3), chess97)

    def chessnow():
        chessboard(ctx, 960, 560, 0.9)
        person(ctx, 700, 760, 1.2, shirt=C['orange'], arm_r=1.0); person(ctx, 1220, 760, 1.2, shirt=C['cyan'], arm_l=1.0)
        for k in range(18):
            x = 120 + k * 100; y = 1000 + (k % 2) * 30
            person(ctx, x, y, 0.55, mono='#20307e')
        n = int(250 * eo(prog(lt, l1 + 1.6, l1 + 3.2)))
        rich(ctx, [(f'{n} million', C['yellow'])], 960, 160, 90, prog(lt, l1 + 1.5, l1 + 1.8))
        rich(ctx, [('users on one chess website', C['white'])], 960, 250, 40, prog(lt, l1 + 2.2, l1 + 2.5), w='normal')
        source_line(ctx, 'Source: Chess.com, 2026', 1, y=1060)
    fade_block(ctx, win(lt, l1 - 0.2, l2), chessnow)

    def humans():
        roles = [('nurse', C['pink']), ('teacher', C['yellow']), ('artist', C['cyan']), ('athlete', C['green'])]
        for k, (lab, col) in enumerate(roles):
            p = eback(prog(lt, l2 + 0.1 + k * 0.4, l2 + 0.4 + k * 0.4))
            x = 330 + k * 420
            if p <= 0: continue
            glow(ctx, x, 560, 220, col, 0.4)
            person(ctx, x, 760, 1.5 * p, shirt=col, arm_r=0.3 + (2.3 if k == 3 else 0.6))
            rich(ctx, [(lab, C['white'])], x, 840, 44, p, pop=False)
            heart(ctx, x + 90, 330, 0.8 * prog(lt, l2 + 2.8 + k * 0.15, l2 + 3.1 + k * 0.15), col)
    fade_block(ctx, win(lt, l2 - 0.2, l3), humans)

    def question():
        bot(ctx, 1300, 860, 2.2, t=t, arm_l=0.3, arm_r=0.3)
        person(ctx, 620, 860, 2.2, shirt=C['orange'])
        rich(ctx, [("Can AI do our jobs?", C['grey'])], 960, 160, 56, prog(lt, l3 + 0.3, l3 + 0.6) * (1 - 0.6 * prog(lt, l3 + 2.0, l3 + 2.4)))
        if lt > l3 + 1.4:
            font(ctx, 56); w_ = ctx.text_extents("Can AI do our jobs?").x_advance
            sk = prog(lt, l3 + 1.4, l3 + 1.8)
            ctx.move_to(960 - w_ / 2, 160); ctx.line_to(960 - w_ / 2 + w_ * sk, 160); ctx.set_line_width(8); src(ctx, C['red']); ctx.stroke()
        rich(ctx, [('Who will AI ', C['white']), ('work for?', C['yellow'])], 960, 300, 90, prog(lt, l3 + 2.4, l3 + 2.8))
    fade_block(ctx, win(lt, l3 - 0.2, l4), question)

    def final():
        glow(ctx, 960, 760, 600, C['yellow'], 0.4)
        hills(ctx, 860, '#3a2a6a', amp=40, phase=0.8)
        person(ctx, 780, 860, 1.6, shirt=C['orange'], arm_l=2.7, arm_r=2.7)
        bot(ctx, 1140, 860, 1.6, t=t, arm_l=0.3, arm_r=1.2)
        te = L[4][1]
        rich(ctx, [('...and finally ', C['white']), ('live.', C['yellow'])], 960, 300, 110, prog(lt, te - 0.6, te - 0.2))
        rich(ctx, [('WHAT IF AI TOOK ALL THE JOBS?', C['grey'])], 960, 440, 40, prog(lt, te + 0.8, te + 1.2), w='normal')
    fade_block(ctx, prog(lt, l4 - 0.2, l4 + 0.3), final)
