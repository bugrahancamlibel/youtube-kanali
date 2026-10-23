import numpy as np, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
from script import timeline

S, LN = timeline()
SR = 44100
import json, os
WARP = len(sys.argv) > 2 and sys.argv[2] == 'warp'
if WARP:
    _wj = json.load(open('vo/warp.json'))
    _DP = np.array([p[0] for p in _wj['pairs']]); _RP = np.array([p[1] for p in _wj['pairs']])
    def Wf(v): return float(np.interp(v, _DP, _RP, right=_RP[-1] + (v - _DP[-1])))
    DUR = _wj['total']
else:
    def Wf(v): return v
    DUR = S[-1]
n = int(SR * DUR) + SR
rng = np.random.default_rng(9)
L = np.zeros(n); R = np.zeros(n)


def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def filt(x, kind, fc, order=2): return sosfilt(butter(order, fc, kind, fs=SR, output='sos'), x)
def ts(ln): return np.arange(int(ln * SR)) / SR


def add(sig, start, gain=1.0, pan=0.0, real=False):
    if not real: start = Wf(start)
    i = int(max(0, start) * SR)
    if i >= n: return
    sig = sig[: n - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def env(ln, a, r):
    m = int(ln * SR); e = np.ones(m)
    ai = max(1, min(m, int(a * SR))); ri = max(1, min(m, int(r * SR)))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri)
    return e


# ------------------------------------------------------------------ score
# chord roots/quality per scene (midi notes, 4-note voicings)
PROG = [
    [[50, 57, 62, 65], [46, 53, 58, 62], [43, 55, 58, 62], [45, 52, 57, 61]],     # 0 mystery  Dm Bb Gm A
    [[41, 57, 60, 65], [48, 55, 60, 64], [50, 57, 62, 65], [46, 53, 58, 62]],     # 1 curious  F C Dm Bb
    [[48, 55, 60, 64], [43, 55, 59, 62], [45, 52, 57, 60], [41, 53, 57, 60]],     # 2 wonder   C G Am F
    [[45, 52, 57, 60], [41, 53, 57, 60], [40, 52, 56, 59], [45, 52, 57, 60]],     # 3 tense    Am F E Am
    [[48, 55, 60, 63], [44, 56, 60, 63], [43, 55, 58, 62], [48, 55, 60, 63]],     # 4 dark     Cm Ab Gm Cm
    [[45, 52, 57, 60], [41, 53, 57, 60], [40, 52, 56, 59], [45, 52, 57, 60]],     # 5 tense
    [[48, 55, 60, 64], [43, 55, 59, 62], [45, 52, 57, 60], [41, 53, 57, 60]],     # 6 hopeful  C G Am F
    [[41, 53, 57, 60], [43, 55, 59, 62], [48, 55, 60, 64], [48, 55, 60, 67]],     # 7 resolve  F G C C
]
BEAT = 60 / 86
BAR = 4 * BEAT
ARP_ON = [False, True, True, True, True, True, True, True]
for si in range(8):
    s0, s1 = Wf(S[si]), Wf(S[si + 1])
    x = s0; k = 0
    while x < s1 - 0.1:
        e = min(s1, x + BAR * 1.0)
        notes = PROG[si][k % 4]
        ln = e - x + 0.8; tt = ts(ln); sig = np.zeros_like(tt)
        for m in notes[1:]:
            for det in (-0.1, 0.0, 0.12):
                f = midi(m) * 2 ** (det / 12)
                sig += 2 * ((tt * f + rng.uniform()) % 1) - 1
        cut = {0: 700, 4: 600}.get(si, 1000)
        sig = filt(sig, 'low', cut) / (len(notes) * 3) * env(ln, 0.6, 0.8)
        add(sig, x - 0.2, 0.17, -0.3, True); add(sig, x - 0.2, 0.17, 0.3, True)
        tt2 = ts(e - x); f = midi(notes[0] - 12)
        pulse = 0.55 + 0.45 * np.cos(np.pi * (tt2 % BEAT) / BEAT) if si not in (0, 4) else 0.8
        add(np.sin(2 * np.pi * f * tt2) * pulse * env(e - x, 0.05, 0.1), x, 0.26, 0.0, True)
        if ARP_ON[si]:
            pat = notes[1:] + [notes[2] + 12]
            y = x; j = 0
            while y < e - 0.05:
                f = midi(pat[j % len(pat)] + 12); tt3 = ts(0.5)
                sg = (np.sin(2 * np.pi * f * tt3) + 0.3 * np.sin(6 * np.pi * f * tt3)) * np.exp(-tt3 * 8)
                add(sg, y, 0.06, 0.5 * np.sin(j * 1.7), True); y += BEAT / 2; j += 1
        x = e; k += 1
    if si in (1, 3, 5):
        for y in np.arange(s0 + 0.5, s1 - 0.5, BEAT / 2):
            tt = ts(0.05)
            add(filt(rng.normal(size=len(tt)), 'high', 7000) * np.exp(-tt * 90), y, 0.022 + 0.012 * ((y / BEAT * 2) % 2), 0.3, True)
    if si in (4,):
        for y in np.arange(s0 + 0.5, s1 - 0.5, BEAT):
            tt = ts(0.3); f = 50 + 60 * np.exp(-tt * 30)
            add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 12), y, 0.18, 0.0, True)


# ------------------------------------------------------------------ sfx
def boom(t0, g=1.0):
    tt = ts(1.4); f = 38 + 90 * np.exp(-tt * 6)
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.8)
    sig += filt(rng.normal(size=len(tt)), 'low', 450) * np.exp(-tt * 10) * 0.6
    add(sig, t0, 0.42 * g)


def pop(t0, f0=900, g=1.0):
    tt = ts(0.14); f = f0 * (1 + 0.8 * np.exp(-tt * 40))
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30), t0, 0.13 * g)


def ding(t0, m, g=1.0):
    tt = ts(0.9); f = midi(m)
    add((np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.76 * f * tt)) * np.exp(-tt * 5), t0, 0.08 * g, 0.2)


def tick(t0, g=1.0):
    tt = ts(0.03); add(np.sin(2 * np.pi * 2300 * tt) * np.exp(-tt * 200), t0, 0.055 * g)


def whoosh(c, ln=0.6, g=1.0):
    tt = ts(ln); e = np.sin(np.pi * tt / ln) ** 2
    add(filt(rng.normal(size=len(tt)), 'band', [400, 3500]) * e, c - ln / 2, 0.09 * g, -0.4)
    add(filt(rng.normal(size=len(tt)), 'band', [500, 3000]) * e, c - ln / 2, 0.09 * g, 0.4)


def glitch(t0, ln, g=1.0):
    tt = ts(ln); sig = np.zeros_like(tt); i = 0
    while i < len(tt):
        seg = int(rng.uniform(0.015, 0.06) * SR); kind = rng.integers(3); part = tt[i:i + seg]
        if kind == 0: s = np.sign(np.sin(2 * np.pi * rng.uniform(150, 2500) * part))
        elif kind == 1:
            hold = int(rng.uniform(4, 40)); s = np.repeat(rng.normal(size=len(part) // hold + 1), hold)[:len(part)]
        else: s = np.zeros_like(part)
        sig[i:i + seg] = s * rng.uniform(0.4, 1.0); i += seg
    add(sig * env(ln, 0.01, 0.05), t0, 0.09 * g, rng.uniform(-0.3, 0.3))


def sweep(t0, ln, f0, f1, g=1.0):
    tt = ts(ln); out = np.zeros_like(tt); noise = rng.normal(size=len(tt)); blk = 2048
    for i in range(0, len(tt), blk):
        fc = f0 + (f1 - f0) * i / len(tt); out[i:i + blk] = filt(noise[i:i + blk], 'band', [fc * 0.8, fc * 1.25])
    add(out * env(ln, 0.1, 0.15), t0, 0.1 * g)


def zap(t0, f0, f1, ln, g=1.0):
    tt = ts(ln); f = np.geomspace(f0, f1, len(tt))
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(ln, 0.01, 0.06), t0, 0.08 * g)


def click(t0, g=1.0):
    tt = ts(0.02); add(rng.normal(size=len(tt)) * np.exp(-tt * 300), t0, 0.2 * g)


def ring(t0, ln):
    tt = ts(ln); s = (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt)) * (np.sin(2 * np.pi * 20 * tt) > 0)
    gate = ((tt % 1.2) < 0.8).astype(float)
    add(s * gate * env(ln, 0.01, 0.1), t0, 0.035)


def coins(t0, k):
    for i in range(k):
        f = 2000 + rng.uniform(-300, 600); tt = ts(0.25)
        add((np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.5 * tt)) * np.exp(-tt * 18), t0 + i * 0.12, 0.04)


def knock(t0, g=1.0):
    tt = ts(0.25); add((np.sin(2 * np.pi * 180 * tt) + filt(rng.normal(size=len(tt)), 'low', 900)) * np.exp(-tt * 25), t0, 0.35 * g)


def crackle(t0, ln):
    tt = ts(ln); s = np.zeros_like(tt)
    for _ in range(int(ln * 60)):
        i = rng.integers(0, len(tt) - 400); s[i:i + 400] += rng.normal(size=400) * np.exp(-np.arange(400) / 60)
    add(filt(s, 'high', 1500), t0, 0.1)


def shutter(t0):
    click(t0, 1.5); click(t0 + 0.06, 1.0); sweep(t0, 0.15, 3000, 6000, 0.6)


def A(si, li, off=0.0): return S[si] + LN[si][li][0] + off
def E(si, li, off=0.0): return S[si] + LN[si][li][1] + off


# transitions (1 crt, 2 zoom, 3 mosaic, 4 shatter, 5 stripes, 6 iris, 7 lids)
b = S
zap(b[1] - .34, 2600, 120, 0.32, 1.1); click(b[1], 1.2); zap(b[1] + 0.02, 150, 1800, 0.3, 0.8)
sweep(b[2] - .45, 0.5, 400, 6000, 1.3); boom(b[2], 0.8); whoosh(b[2] + 0.15, 0.5, 0.7)
glitch(b[3] - .32, 0.62, 1.4); sweep(b[3] - .32, 0.6, 3000, 600, 0.7)
crackle(b[4] - .6, 0.4); boom(b[4] - .25, 0.9)
for k in range(12): click(b[4] - .2 + k * 0.05 + rng.uniform(0, 0.03), 0.5)
for k in range(3): whoosh(b[5] - .3 + k * 0.18, 0.32, 0.9); pop(b[5] - .25 + k * 0.18, 500 + k * 250, 0.8)
zap(b[6] - .36, 300, 2400, 0.6, 0.9); ding(b[6], 86, 1.1); whoosh(b[6], 0.5, 0.7)
whoosh(b[7] - .2, 0.35, 0.8); boom(b[7], 0.5); whoosh(b[7] + 0.2, 0.35, 0.6)

# scene 0
for k, st in enumerate((1.6, 3.0, 4.3)): pop(A(0, 0, st), 700 + k * 150); ding(A(0, 0, st + 0.1), 79 + k * 3, 0.6)
pop(A(0, 1, 0.3), 500, 1.2)
for k in range(40): tick(A(0, 1, 1.5 + k * 0.15), 0.35)
pop(A(0, 1, 5.1), 800); ding(A(0, 1, 5.2), 72, 0.9)
sweep(A(0, 2, 0.2), 1.2, 200, 1200, 0.7); zap(A(0, 2, 1.6), 300, 2400, 0.7, 1.0)
click(A(0, 2, 2.7), 1.4); boom(A(0, 2, 2.8), 0.7); pop(A(0, 2, 3.3), 900)
for k in range(8): click(A(0, 3, 1.7 + k * 0.32), 0.9); ding(A(0, 3, 1.75 + k * 0.32), 84 - k, 0.35)
boom(A(0, 3, 4.6), 1.0)
boom(E(0, 3, 0.2), 1.1); ding(E(0, 3, 0.35), 74, 1.2); ding(E(0, 3, 0.55), 81, 1.0)
# scene 1
pop(A(1, 0, 0.6), 600, 1.0)
for k in range(3): whoosh(A(1, 0, 1.9 + k * 0.6), 0.6, 0.5); pop(A(1, 0, 2.6 + k * 0.6), 700 + k * 100)
for k in range(3): click(A(1, 0, 5.1 + k * 0.3), 0.9)
whoosh(A(1, 0, 6.6), 1.0, 0.6); pop(A(1, 0, 7.4), 600)
ding(A(1, 1, 0.5), 84, 0.8); click(A(1, 1, 1.5), 1.2)
pop(A(1, 1, 3.0), 800); ding(A(1, 1, 3.1), 79, 0.7); pop(A(1, 1, 4.3), 500)
for k in range(30): tick(A(1, 1, 5.6 + k * 0.04), 0.4)
glitch(A(1, 1, 6.9), 0.25, 0.8)
# scene 2
pop(A(2, 0, 0.4), 600); pop(A(2, 0, 1.7), 900); sweep(A(2, 0, 1.8), 1.0, 400, 2400, 0.5)
sweep(A(2, 0, 4.4), 2.0, 300, 900, 0.5); ding(A(2, 0, 5.8), 86, 0.8)
pop(A(2, 1, 0.3), 600)
for k in range(6): tick(A(2, 1, 1.6 + k * 0.12), 0.8)
pop(A(2, 1, 4.3), 800); click(A(2, 1, 5.3), 1.2); ding(A(2, 1, 5.4), 79, 0.8)
for k in range(4): glitch(A(2, 2, 1.6 + k * 0.6), 0.2, 0.9); pop(A(2, 2, 1.6 + k * 0.6), 400, 0.6)
pop(A(2, 3, 0.4), 700); pop(A(2, 3, 1.4), 900); sweep(A(2, 3, 3.4), 2.4, 1600, 200, 0.7)
for k in range(20): pop(A(2, 3, 3.7 + k * 0.06), 500 + k * 30, 0.25)
# scene 3
sweep(A(3, 0, 1.2), 2.8, 2000, 300, 0.6)
for k in range(50): tick(A(3, 1, 0.6 + k * 0.1), 0.3)
boom(A(3, 1, 6.2), 0.5); pop(A(3, 1, 7.0), 800); pop(A(3, 1, 8.6), 900)
pop(A(3, 2, 1.0), 1000); pop(A(3, 2, 3.2), 1100); ding(A(3, 2, 3.8), 88, 0.7)
sweep(A(3, 3, 0.4), 2.8, 300, 1500, 0.5); ding(A(3, 3, 3.0), 76, 1.0); boom(A(3, 3, 3.0), 0.5)
# scene 4
click(A(4, 0, 0.9), 1.3); boom(A(4, 0, 1.0), 0.9)
for k in range(3): pop(A(4, 1, 0.3 + k * 0.25), 600 + k * 120)
for k in range(3): click(A(4, 1, 1.7 + k * 1.2), 1.3); zap(A(4, 1, 1.8 + k * 1.2), 1600, 200, 0.3, 0.6)
pop(A(4, 2, 0.3), 700); whoosh(A(4, 2, 1.5), 0.6, 0.6); pop(A(4, 2, 2.7), 800)
for k in range(3): glitch(A(4, 2, 3.4 + k * 0.4), 0.15, 0.8)
for k in range(24): pop(A(4, 3, 0.6 + k * 0.3), 1200 + (k % 3) * 200, 0.2)
boom(A(4, 3, 5.5), 0.9); ding(A(4, 3, 5.6), 74, 0.8)
# scene 5
pop(A(5, 0, 0.3), 500, 1.2); coins(A(5, 0, 0.5), 6)
sweep(A(5, 0, 2.0), 2.5, 300, 1600, 0.5); zap(A(5, 0, 5.7), 300, 2400, 0.6, 0.8)
for k in range(25): pop(A(5, 1, 0.2 + k * 0.05), 900 + k * 10, 0.25)
for k in range(30): tick(A(5, 1, 0.6 + k * 0.09), 0.3)
for k in range(10): click(A(5, 1, 4.0 + k * 0.12), 0.5)
pop(A(5, 1, 5.0), 600)
pop(A(5, 2, 0.6), 600); pop(A(5, 2, 1.6), 800); coins(A(5, 2, 1.7), 8); sweep(A(5, 2, 3.0), 1.0, 200, 600, 0.4)
sweep(A(5, 3, -0.2), 1.0, 200, 1200, 0.7); click(A(5, 3, 1.0), 1.3); zap(A(5, 3, 1.1), 300, 2600, 0.8, 0.9)
coins(A(5, 3, 1.4), 18); boom(A(5, 3, 2.2), 0.8)
pop(A(5, 4, 0.5), 700); crackle(A(5, 4, 0.7), 0.5); pop(A(5, 4, 2.5), 600); crackle(A(5, 4, 4.0), 0.5); boom(A(5, 4, 4.1), 0.5)
# scene 6
pop(A(6, 0, 0.5), 600, 1.2); ding(A(6, 0, 0.7), 84, 1.0)
pop(A(6, 0, 3.1), 800); ding(A(6, 0, 3.2), 88, 0.8)
for k in range(3): pop(A(6, 0, 4.4 + k * 0.4), 900 + k * 100)
sweep(A(6, 1, 0.2), 1.0, 300, 1800, 0.5)
for k in range(4): pop(A(6, 1, 1.7 + k * 0.4), 1300, 0.3)
pop(A(6, 1, 2.5), 700)
sweep(A(6, 2, 0.1), 0.8, 300, 2000, 0.6)
for k, st in enumerate((0.4, 1.0, 1.8, 3.4)): pop(A(6, 2, st), 700 + k * 100); ding(A(6, 2, st + 0.05), 76 + k * 2, 0.5)
for k in range(8): pop(A(6, 3, 0.1 + k * 0.12), 600 + k * 60, 0.6)
for k in range(8): click(A(6, 3, 1.8 + k * 0.55), 0.8); ding(A(6, 3, 1.85 + k * 0.55), 79 + (k % 4) * 2, 0.35)
# scene 7
for k in range(11): tick(A(7, 0, 0.3 + k * 0.06), 0.8)
pop(A(7, 0, 0.3), 600); sweep(A(7, 0, 3.4), 0.8, 300, 1500, 0.6)
whoosh(A(7, 1, 0.2), 0.8, 0.6)
for k in range(3): pop(A(7, 1, 1.0 + k * 1.2), 700 + k * 150); ding(A(7, 1, 1.1 + k * 1.2), [76, 79, 84][k], 0.7)
for k in range(40): knock(A(7, 2, 0.3 + k * 0.14), 0.25)
sweep(A(7, 2, 0.2), 5.0, 200, 900, 0.4)
pop(A(7, 3, 0.3), 500); click(A(7, 3, 1.4), 1.0)
boom(E(7, 3, 0.4), 1.0)
for k, m in enumerate((72, 76, 79, 84)): ding(E(7, 3, 0.5 + k * 0.08), m, 1.1)

mix = np.stack([L, R], 1)
mix = filt(mix.T, 'high', 30).T
fade = np.ones(n); fo = int(2.0 * SR); end = int(DUR * SR)
fade[end - fo:end] = np.linspace(1, 0, fo); fade[end:] = 0
mix *= fade[:, None]
mix = mix[:end]
mix = np.tanh(mix * 1.5) / np.tanh(1.5)
mix /= np.max(np.abs(mix)) / 0.89
wavfile.write(sys.argv[1] if len(sys.argv) > 1 else 'music_long.wav', SR, (mix * 32767).astype(np.int16))
print('ok', mix.shape[0] / SR)
