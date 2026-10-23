"""Repurpose a segment of a 16:9 long video into a 9:16 Short with hook title + burned captions.

usage: python3 make_short.py spec.json
spec = {
  "video": "long.mp4", "out": "short.mp4", "start": 84.0, "end": 117.0,
  "hook": [["HE SENT ", "#ffffff"], ["$25 MILLION", "#ff4f81"]],   # list of lines; each line list of [text, color]
  "hook2": [[["TO A ", "#ffffff"], ["DEEPFAKE", "#3ee0ff"]]],
  "captions": [[t0, t1, "text"], ...]     # absolute times in the long video
  "footer": "Full video on the channel"
}
"""
import json, sys, os, subprocess, math, tempfile
import cairo

W, H = 1080, 1920
CLIP_W = 1300                      # scaled clip width before cropping to 1080
CLIP_H = int(round(CLIP_W * 9 / 16 / 2)) * 2
CLIP_Y = 600


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def text_png(path, lines, size, maxw=980, stroke=10, box=False, weight=cairo.FONT_WEIGHT_BOLD):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, 600); c = cairo.Context(s)
    c.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, weight)
    y = 0; rows = []
    for parts in lines:
        c.set_font_size(size)
        tw = sum(c.text_extents(t).x_advance for t, _ in parts)
        sz = size * min(1.0, maxw / max(tw, 1)); c.set_font_size(sz)
        tw = sum(c.text_extents(t).x_advance for t, _ in parts)
        rows.append((parts, sz, tw))
    tot = sum(sz * 1.22 for _, sz, _ in rows)
    y = 300 - tot / 2
    if box:
        mw = max(tw for _, _, tw in rows)
        c.new_path(); r = 26; x0, y0, w0, h0 = W / 2 - mw / 2 - 34, y - 14, mw + 68, tot + 30
        c.arc(x0 + w0 - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w0 - r, y0 + h0 - r, r, 0, math.pi / 2)
        c.arc(x0 + r, y0 + h0 - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
        c.close_path(); c.set_source_rgba(0.02, 0.03, 0.12, 0.72); c.fill()
    for parts, sz, tw in rows:
        c.set_font_size(sz)
        base = y + sz * 0.95
        x = W / 2 - tw / 2
        for t, col in parts:
            c.move_to(x, base); c.text_path(t)
            if stroke:
                c.set_source_rgba(0.02, 0.03, 0.12, 0.95); c.set_line_width(stroke); c.set_line_join(cairo.LINE_JOIN_ROUND)
                c.stroke_preserve()
            c.set_source_rgb(*hexc(col)); c.fill()
            x += c.text_extents(t).x_advance
        y += sz * 1.22
    s.write_to_png(path)


def chunks(captions, start, end, maxw=4):
    out = []
    for t0, t1, txt in captions:
        if t1 < start or t0 > end: continue
        words = txt.split()
        n = math.ceil(len(words) / maxw); per = math.ceil(len(words) / n)
        groups = [words[i:i + per] for i in range(0, len(words), per)]
        total = sum(len(' '.join(g)) for g in groups)
        tt = t0
        for g in groups:
            d = (t1 - t0) * len(' '.join(g)) / total
            out.append((max(start, tt) - start, min(end, tt + d) - start, ' '.join(g)))
            tt += d
    return [c for c in out if c[1] > c[0]]


def main():
    spec = json.load(open(sys.argv[1]))
    tmp = tempfile.mkdtemp(prefix='short_', dir=os.path.dirname(os.path.abspath(sys.argv[1])))
    text_png(f'{tmp}/hook.png', spec['hook'], 96, stroke=12)
    inputs = ['-i', f'{tmp}/hook.png']
    overlays = []
    if spec.get('hook2'):
        text_png(f'{tmp}/hook2.png', spec['hook2'], 96, stroke=12)
        inputs += ['-i', f'{tmp}/hook2.png']
    text_png(f'{tmp}/footer.png', [[(spec.get('footer', 'Full video on the channel'), '#9aaad6')]], 40, stroke=0,
             weight=cairo.FONT_WEIGHT_NORMAL)
    inputs += ['-i', f'{tmp}/footer.png']
    hold = float(spec.get('end_hold', 1.8))
    text_png(f'{tmp}/endcard.png', [[(spec.get('end_card', 'WATCH THE FULL VIDEO'), '#ffd23f')],
                                     [(spec.get('end_card2', 'on the channel'), '#ffffff')]], 90, stroke=12)
    inputs += ['-i', f'{tmp}/endcard.png']
    caps = chunks(spec['captions'], spec['start'], spec['end'])
    for k, (a, b, txt) in enumerate(caps):
        words = txt.upper().split()
        # highlight the longest word in yellow
        hi = max(range(len(words)), key=lambda i: len(words[i]))
        parts = []
        for i, w in enumerate(words):
            parts.append((w + (' ' if i < len(words) - 1 else ''), '#ffd23f' if i == hi else '#ffffff'))
        text_png(f'{tmp}/c{k:03d}.png', [parts], 74, stroke=12)
        inputs += ['-i', f'{tmp}/c{k:03d}.png']
    dur = spec['end'] - spec['start']
    sw = CLIP_W
    fc = []
    # main segment + a frozen 'hero' frame (freeze_at, absolute time; default = end) held for the end card
    F = float(spec.get('freeze_at', spec['end'] - 0.05))
    fc.append(f"[0:v]split=2[src1][src2]")
    fc.append(f"[src1]trim=start={spec['start']}:end={spec['end']},setpts=PTS-STARTPTS,fps=30[mainv]")
    fc.append(f"[src2]trim=start={F:.3f}:duration=0.04,setpts=PTS-STARTPTS,fps=30,"
              f"tpad=stop_mode=clone:stop_duration={hold:.3f},trim=duration={hold:.3f},setpts=PTS-STARTPTS[frz]")
    fc.append(f"[mainv][frz]concat=n=2:v=1:a=0,split=2[v1][v2]")
    fc.append(f"[v1]scale=-2:{H},crop={W}:{H},boxblur=28:3,eq=brightness=-0.18:saturation=1.1[bg]")
    fc.append(f"[v2]scale={sw}:{CLIP_H},crop={W}:{CLIP_H}[fg]")
    fc.append(f"[bg][fg]overlay=0:{CLIP_Y}[b0]")
    idx = 1; last = 'b0'
    hook_end = spec.get('hook_until', dur)
    fc.append(f"[{last}][{idx}:v]overlay=0:{CLIP_Y - 600 + 20}:enable='lt(t,{hook_end})'[b1]"); last = 'b1'; idx += 1
    if spec.get('hook2'):
        fc.append(f"[{last}][{idx}:v]overlay=0:{CLIP_Y - 600 + 20}:enable='gte(t,{hook_end})'[b2]"); last = 'b2'; idx += 1
    fc.append(f"[{last}][{idx}:v]overlay=0:{1880 - 300 - 30}[bf]"); last = 'bf'; idx += 1
    end_idx = idx; idx += 1
    for k, (a, b, txt) in enumerate(caps):
        nm = f'c{k}'
        fc.append(f"[{last}][{idx}:v]overlay=0:{CLIP_Y + CLIP_H - 300 + 230}:enable='between(t,{a:.3f},{b:.3f})'[{nm}]")
        last = nm; idx += 1
    # end card: freeze the last frame, dim it, show call-to-action
    fc.append(f"[{last}]drawbox=x=0:y=0:w=iw:h=ih:color=black@0.55:t=fill:enable='gte(t,{dur:.3f})'[tp]")
    fc.append(f"[tp][{end_idx}:v]overlay=0:{H // 2 - 300}:enable='gte(t,{dur:.3f})'[te]")
    fc.append(f"[te]format=yuv420p[vout]")
    fc.append(f"[0:a]atrim=start={spec['start']}:end={spec['end']},asetpts=PTS-STARTPTS,afade=t=in:d=0.15,"
              f"afade=t=out:st={max(0, dur - 0.35):.3f}:d=0.35,apad=pad_dur={hold:.3f}[aout]")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', spec['video']] + [x for i in range(0, len(inputs), 2)
                                                                       for x in (inputs[i], inputs[i + 1])]
    cmd += ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]', '-r', '30', '-c:v', 'libx264',
            '-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '192k', '-t', f'{dur + hold:.3f}',
            '-movflags', '+faststart', spec['out']]
    # still images need -loop to stay for full duration
    full = ['ffmpeg', '-y', '-loglevel', 'error', '-i', spec['video']]
    for i in range(0, len(inputs), 2):
        full += ['-loop', '1', '-t', f'{dur + hold:.3f}', inputs[i], inputs[i + 1]]
    full += cmd[cmd.index('-filter_complex'):]
    subprocess.run(full, check=True)
    print('wrote', spec['out'], 'captions', len(caps))


if __name__ == '__main__':
    main()
