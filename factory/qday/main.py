import sys, json, subprocess
from props_q import *
from script import SCRIPT, timeline
from scenes_q import s0, s1, s2, s3, s4, s5, s6, s7

SCENES = [s0, s1, s2, s3, s4, s5, s6, s7]
S, LINES = timeline()
DUR = S[-1]
SUBS = True

# boundary b (between scene b-1 and b): kind, half length, extra params
TRANS = {1: ('crt', 0.34, {}), 2: ('zoom', 0.45, {'c': (640, 520)}), 3: ('mosaic', 0.34, {}),
         4: ('shatter', 0.6, {}), 5: ('stripes', 0.42, {}), 6: ('iris', 0.36, {'c': (640, 520)}), 7: ('lids', 0.36, {})}

OUT_S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
IN_S = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)


def ein(x): x = clamp(x); return x ** 3


def render_to(surf, i, t):
    c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
    SCENES[i](c, t - S[i], t, LINES[i]); surf.flush(); return surf


def paint_surf(ctx, surf, alpha=1.0, sx=1.0, sy=None, cx=W / 2, cy=H / 2):
    sy = sx if sy is None else sy
    ctx.save(); ctx.translate(cx, cy); ctx.scale(sx, sy); ctx.translate(-cx, -cy)
    ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(alpha); ctx.restore()


def pixelate(ctx, surf, block, alpha=1.0):
    if block <= 1.05:
        ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(alpha); return
    sw, sh = max(1, int(W / block)), max(1, int(H / block))
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    sc = cairo.Context(small); sc.scale(sw / W, sh / H)
    sc.set_source_surface(surf, 0, 0); sc.get_source().set_filter(cairo.FILTER_GOOD); sc.paint()
    ctx.save(); ctx.scale(W / sw, H / sh); ctx.set_source_surface(small, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_NEAREST); ctx.paint_with_alpha(alpha); ctx.restore()


def t_mosaic(ctx, o, i, x, t, P):
    blk = 1 + 90 * (ein(x / 0.5) if x < 0.5 else ein((1 - x) / 0.5))
    pixelate(ctx, o, blk)
    mix = ss((x - 0.4) / 0.2)
    if mix > 0: pixelate(ctx, i, blk, mix)
    peak = math.sin(math.pi * x) ** 4
    if peak > 0.05:
        rnd = random.Random(int(t * 30))
        for _ in range(8):
            y = rnd.uniform(0, H); h = rnd.uniform(14, 90)
            ctx.rectangle(0, y, W, h); src(ctx, rnd.choice([C['cyan'], C['pink'], C['yellow']]), 0.35 * peak); ctx.fill()


def t_iris(ctx, o, i, x, t, P):
    px, py = P['c']
    paint_surf(ctx, o, 1.0, 1 + 0.06 * x, cx=px, cy=py)
    r = (ss(x) ** 1.4) * 2300
    if r > 1:
        ctx.save(); ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.clip()
        paint_surf(ctx, i, 1.0, 1.12 - 0.12 * x, cx=px, cy=py); ctx.restore()
        ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.set_line_width(36); src(ctx, C['yellow'], 0.35); ctx.stroke()
        ctx.new_path(); ctx.arc(px, py, r, 0, 2 * math.pi); ctx.set_line_width(12); src(ctx, '#fff3c8', 0.95); ctx.stroke()


def t_zoom(ctx, o, i, x, t, P):
    px, py = P['c']
    if x < 0.55:
        k = x / 0.55
        paint_surf(ctx, o, 1.0, math.exp(math.log(60) * k ** 2.0), cx=px, cy=py)
        d = ss((k - 0.55) / 0.45)
        if d > 0: ctx.set_source_rgba(0.05, 0.04, 0.12, d); ctx.paint()
    else:
        k = (x - 0.55) / 0.45
        ctx.set_source_rgba(0.05, 0.04, 0.12, 1); ctx.paint()
        r = eo(k) * 1250
        if r > 1:
            ctx.save(); ctx.new_path(); ctx.arc(W / 2, H / 2, r, 0, 2 * math.pi); ctx.clip()
            paint_surf(ctx, i, 1.0, 1.35 - 0.35 * eo(k)); ctx.restore()
            ctx.new_path(); ctx.arc(W / 2, H / 2, r, 0, 2 * math.pi); ctx.set_line_width(14); src(ctx, C['cyan'], 1 - k); ctx.stroke()
        glow(ctx, W / 2, H / 2, 600, C['cyan'], 0.5 * (1 - k))


def crt(ctx, surf, k):
    if k < 0.62:
        sy = 1 - ein(k / 0.62) * 0.995; sx = 1.0 + 0.04 * (k / 0.62)
    else:
        sy = 0.005; sx = 1.04 * (1 - ss((k - 0.62) / 0.38) * 0.99)
    paint_surf(ctx, surf, 1.0, sx, sy)
    flash = clamp(k * 1.3)
    ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(sx, sy)
    ctx.rectangle(-W / 2, -H / 2, W, H); ctx.set_source_rgba(0.85, 0.97, 1, 0.85 * flash); ctx.fill(); ctx.restore()
    glow(ctx, W / 2, H / 2, max(60, 900 * sx), C['cyan'], 0.6 * flash)


def t_crt(ctx, o, i, x, t, P):
    ctx.set_source_rgb(0.01, 0.01, 0.04); ctx.paint()
    if x < 0.5: crt(ctx, o, x / 0.5)
    else: crt(ctx, i, 1 - (x - 0.5) / 0.5)
    a = math.sin(math.pi * x) * 0.25
    for y in range(0, H, 8): ctx.rectangle(0, y, W, 3)
    ctx.set_source_rgba(0, 0, 0, a); ctx.fill()


def band(ctx, E):
    ctx.new_path(); ctx.move_to(-2500, 0); ctx.line_to(E, 0); ctx.line_to(E - 0.6 * H, H); ctx.line_to(-2500, H); ctx.close_path()


def t_stripes(ctx, o, i, x, t, P):
    ctx.set_source_surface(o, 0, 0); ctx.paint()
    edges = [lerp(-300, W + 0.6 * H + 300, ss(clamp((x - j * 0.12) / 0.64))) for j in range(4)]
    for j, col in enumerate((C['pink'], C['yellow'], C['cyan'])):
        band(ctx, edges[j]); src(ctx, col); ctx.fill()
        ctx.new_path(); ctx.move_to(edges[j], 0); ctx.line_to(edges[j] - 0.6 * H, H)
        ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.5); ctx.stroke()
    ctx.save(); band(ctx, edges[3]); ctx.clip(); ctx.set_source_surface(i, 0, 0); ctx.paint(); ctx.restore()


def almond(ctx, cx, cy, hw, h):
    ctx.move_to(cx - hw, cy)
    ctx.curve_to(cx - hw * 0.5, cy - h / 0.75, cx + hw * 0.5, cy - h / 0.75, cx + hw, cy)
    ctx.curve_to(cx + hw * 0.5, cy + h / 0.75, cx - hw * 0.5, cy + h / 0.75, cx - hw, cy)
    ctx.close_path()


def t_lids(ctx, o, i, x, t, P):
    if x < 0.5:
        ctx.set_source_surface(o, 0, 0); ctx.paint(); h = 900 * (1 - ein(x / 0.5))
    else:
        ctx.set_source_surface(i, 0, 0); ctx.paint(); k = (x - 0.5) / 0.5
        h = 900 * eback(k, 1.2) * (1 - 0.35 * math.sin(math.pi * clamp(k / 0.5)) * (k < 0.5))
    ctx.new_path(); ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(-10, -10, W + 20, H + 20); almond(ctx, W / 2, H / 2, 1500, max(h, 0.5))
    src(ctx, '#05081a'); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    if h < 860:
        ctx.new_path(); almond(ctx, W / 2, H / 2, 1500, max(h, 0.5)); ctx.set_line_width(14); src(ctx, '#2a3a8a'); ctx.stroke()


random.seed(77)
_pts = {}
GX, GY = 9, 6
for gi in range(GX + 1):
    for gj in range(GY + 1):
        jx = 0 if gi in (0, GX) else random.uniform(-70, 70)
        jy = 0 if gj in (0, GY) else random.uniform(-60, 60)
        _pts[(gi, gj)] = (gi * W / GX + jx, gj * H / GY + jy)
SHARDS = []
for gi in range(GX):
    for gj in range(GY):
        a, b, c, d = _pts[(gi, gj)], _pts[(gi + 1, gj)], _pts[(gi + 1, gj + 1)], _pts[(gi, gj + 1)]
        for tri in ((a, b, c), (a, c, d)) if random.random() < 0.5 else ((a, b, d), (b, c, d)):
            cx_ = sum(p[0] for p in tri) / 3; cy_ = sum(p[1] for p in tri) / 3
            SHARDS.append((tri, cx_, cy_, random.uniform(-2.5, 2.5), random.uniform(-200, 200), random.uniform(0, 0.25)))


def t_shatter(ctx, o, i, x, t, P):
    ctx.set_source_surface(i, 0, 0); ctx.paint()
    ctx.set_source_rgba(0, 0, 0.05, 0.5 * (1 - x)); ctx.paint()
    crack = clamp(x / 0.3)
    for (tri, cx_, cy_, rot, vx, delay) in SHARDS:
        k = clamp((x - 0.3 - delay * (1 - abs(cx_ - W / 2) / W)) / 0.7)
        dy = 2600 * k * k; dx = vx * k
        ctx.save(); ctx.translate(cx_ + dx, cy_ + dy); ctx.rotate(rot * k); ctx.scale(1 - 0.3 * k, 1 - 0.3 * k)
        ctx.translate(-cx_, -cy_)
        ctx.new_path(); ctx.move_to(*tri[0]); ctx.line_to(*tri[1]); ctx.line_to(*tri[2]); ctx.close_path()
        path = ctx.copy_path()
        ctx.save(); ctx.clip(); ctx.set_source_surface(o, 0, 0); ctx.paint()
        ctx.set_source_rgba(1, 1, 1, 0.08 * k); ctx.paint(); ctx.restore()
        ctx.new_path(); ctx.append_path(path); ctx.set_line_width(3); ctx.set_source_rgba(1, 1, 1, 0.8 * crack * (1 - k))
        ctx.stroke()
        ctx.restore()


TFUN = dict(mosaic=t_mosaic, iris=t_iris, zoom=t_zoom, crt=t_crt, stripes=t_stripes, lids=t_lids, shatter=t_shatter)

ALL_LINES = []
for si, ls in enumerate(LINES):
    for li, (a, b) in enumerate(ls):
        ALL_LINES.append((S[si] + a, S[si] + b, SCRIPT[si][li]))


def wrap(ctx, txt, maxw):
    words = txt.split(); lines = [[]]
    for w in words:
        test = ' '.join(lines[-1] + [w])
        if ctx.text_extents(test).x_advance > maxw and lines[-1]: lines.append([w])
        else: lines[-1].append(w)
    return [' '.join(l) for l in lines]


def subtitle(ctx, t):
    for (a, b, txt) in ALL_LINES[:-1]:
        if a - 0.05 <= t < b + 0.3:
            al = prog(t, a - 0.05, a + 0.1) * (1 - prog(t, b + 0.15, b + 0.3))
            font(ctx, 38, 'normal')
            rows = wrap(ctx, txt, 1300)
            lh = 50; tot = lh * len(rows)
            y0 = 1000 - tot
            mw = max(ctx.text_extents(r).x_advance for r in rows)
            rrect(ctx, W / 2 - mw / 2 - 26, y0 - 8, mw + 52, tot + 26, 18); ctx.set_source_rgba(0.02, 0.03, 0.12, 0.62 * al)
            ctx.fill()
            for k, r in enumerate(rows):
                w = ctx.text_extents(r).x_advance
                ctx.move_to(W / 2 - w / 2, y0 + 34 + k * lh); ctx.set_source_rgba(1, 1, 1, al); ctx.show_text(r)
            return


def frame(ctx, t):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    done = False
    for b, (kind, hl, P) in TRANS.items():
        if S[b] - hl <= t < S[b] + hl:
            x = (t - (S[b] - hl)) / (2 * hl)
            render_to(OUT_S, b - 1, t)
            render_to(IN_S, b, S[b] + (t - S[b] + hl) / 2)
            TFUN[kind](ctx, OUT_S, IN_S, x, t, P); done = True; break
    if not done:
        idx = max(i for i in range(8) if t >= S[i])
        ctx.push_group(); SCENES[idx](ctx, t - S[idx], t, LINES[idx]); ctx.pop_group_to_source(); ctx.paint()
    vignette(ctx)
    if SUBS: subtitle(ctx, t)


def main():
    out, mode = sys.argv[1], sys.argv[2]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    if mode == 'stills':
        for tv in [float(v) for v in sys.argv[3].split(',')]:
            frame(ctx, tv); surf.write_to_png(f'{out}/L_{tv:06.2f}.png')
        return
    if mode == 'info':
        json.dump({'S': S, 'lines': ALL_LINES, 'dur': DUR}, open(out, 'w'), indent=1); return
    global SUBS
    tau = lambda tr: tr
    if mode == 'warp':
        import numpy as np
        SUBS = False
        wj = json.load(open('vo/warp.json'))
        Dp = np.array([p[0] for p in wj['pairs']]); Rp = np.array([p[1] for p in wj['pairs']])
        tau = lambda tr: float(np.interp(tr, Rp, Dp))
        if sys.argv[3] == 'n':
            print(int(round(wj['total'] * FPS))); return
        if sys.argv[3] == 'stills':
            for tv in [float(v) for v in sys.argv[4].split(',')]:
                frame(ctx, tau(tv)); surf.write_to_png(f'{out}/W_{tv:06.2f}.png')
            return
    f0, f1 = int(sys.argv[3]), int(sys.argv[4])
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                          '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        frame(ctx, tau(f / FPS)); surf.flush(); p.stdin.write(bytes(surf.get_data()))
        if f % 150 == 0: print('frame', f, flush=True)
    p.stdin.close(); p.wait(); print('DONE', flush=True)


if __name__ == '__main__':
    main()
