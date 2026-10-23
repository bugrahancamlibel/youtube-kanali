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
    [[45, 52, 57, 60], [41, 53, 57, 60], [40, 52, 56, 59], [45, 52, 57, 60]],     # 1 tense    Am F E Am
    [[48, 55, 60, 63], [44, 56, 60, 63], [43, 55, 58, 62], [48, 55, 60, 63]],     # 2 dark     Cm Ab Gm Cm
    [[45, 52, 57, 60], [41, 53, 57, 60], [40, 52, 56, 59], [45, 52, 57, 60]],     # 3 tense
    [[48, 55, 60, 63], [44, 56, 60, 63], [43, 55, 58, 62], [48, 55, 60, 63]],     # 4 dark
    [[41, 57, 60, 65], [48, 55, 60, 64], [50, 57, 62, 65], [46, 53, 58, 62]],     # 5 curious  F C Dm Bb
    [[48, 55, 60, 64], [43, 55, 59, 62], [45, 52, 57, 60], [41, 53, 57, 60]],     # 6 wonder   C G Am F
    [[41, 53, 57, 60], [43, 55, 59, 62], [48, 55, 60, 64], [48, 55, 60, 67]],     # 7 resolve  F G C C
]
BEAT = 60 / 80
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
        cut = {0: 650, 2: 600, 4: 600}.get(si, 900)
        sig = filt(sig, 'low', cut) / (len(notes) * 3) * env(ln, 0.6, 0.8)
        add(sig, x - 0.2, 0.17, -0.3, True); add(sig, x - 0.2, 0.17, 0.3, True)
        tt2 = ts(e - x); f = midi(notes[0] - 12)
        pulse = 0.55 + 0.45 * np.cos(np.pi * (tt2 % BEAT) / BEAT) if si not in (0, 2, 4) else 0.8
        add(np.sin(2 * np.pi * f * tt2) * pulse * env(e - x, 0.05, 0.1), x, 0.26, 0.0, True)
        if ARP_ON[si]:
            pat = notes[1:] + [notes[2] + 12]
            y = x; j = 0
            while y < e - 0.05:
                f = midi(pat[j % len(pat)] + 12); tt3 = ts(0.5)
                sg = (np.sin(2 * np.pi * f * tt3) + 0.3 * np.sin(6 * np.pi * f * tt3)) * np.exp(-tt3 * 8)
                add(sg, y, 0.06, 0.5 * np.sin(j * 1.7), True); y += BEAT / 2; j += 1
        x = e; k += 1
    if si in (1, 3, 6):
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


# transitions (1 iris, 2 stripes, 3 lids, 4 shatter, 5 zoom, 6 crt, 7 mosaic)
b = S
zap(b[1] - .36, 300, 2400, 0.6, 0.9); ding(b[1], 86, 1.1); whoosh(b[1], 0.5, 0.7)
for k in range(3): whoosh(b[2] - .3 + k * 0.18, 0.32, 0.9); pop(b[2] - .25 + k * 0.18, 500 + k * 250, 0.8)
whoosh(b[3] - .2, 0.35, 0.8); boom(b[3], 0.5); whoosh(b[3] + 0.2, 0.35, 0.6)
crackle(b[4] - .6, 0.5); boom(b[4] - .25, 1.0)
for k in range(12): click(b[4] - .2 + k * 0.05 + rng.uniform(0, 0.03), 0.5)
sweep(b[5] - .45, 0.5, 400, 6000, 1.3); boom(b[5], 0.8); whoosh(b[5] + 0.15, 0.5, 0.7)
zap(b[6] - .34, 2600, 120, 0.32, 1.1); click(b[6], 1.2); zap(b[6] + 0.02, 150, 1800, 0.3, 0.8)
glitch(b[7] - .32, 0.62, 1.4); sweep(b[7] - .32, 0.6, 3000, 600, 0.7)


def creak(t0, ln=1.2, g=1.0):
    tt = ts(ln); f = 60 + 25 * np.sin(2 * np.pi * 3 * tt) + 15 * rng.normal(size=len(tt)).cumsum() / np.sqrt(np.arange(1, len(tt) + 1))
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / ln) ** 2
    sig += filt(rng.normal(size=len(tt)), 'band', [200, 900]) * 0.3 * np.sin(np.pi * tt / ln) ** 2
    add(sig, t0, 0.12 * g)


def splash(t0, g=1.0):
    tt = ts(1.0); add(filt(rng.normal(size=len(tt)), 'band', [300, 4000]) * np.exp(-tt * 4), t0, 0.12 * g)
    boom(t0, 0.5 * g)


def bubbles(t0, n, g=1.0):
    for k in range(n):
        tt = ts(0.08); f = rng.uniform(500, 1400) * (1 + 1.5 * tt / 0.08)
        add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 40), t0 + k * rng.uniform(0.05, 0.15), 0.05 * g, rng.uniform(-0.5, 0.5))


# scene 0
sweep(0.2, 2.4, 200, 1200, 0.5); pop(A(0, 0, 2.2), 600); ding(A(0, 0, 2.3), 79, 0.7)
pop(A(0, 0, 3.5), 800); pop(A(0, 0, 3.9), 900)
whoosh(A(0, 0, 5.2), 0.6, 0.7); sweep(A(0, 0, 5.7), 0.6, 300, 1500, 0.6); creak(A(0, 0, 7.4), 2.0, 1.2)
pop(A(0, 1, 0.3), 600, 1.2); crackle(A(0, 1, 2.0), 0.2); boom(A(0, 1, 2.1), 0.9)
creak(A(0, 2, 1.0), 1.5)
for k in range(3): crackle(A(0, 2, 1.6 + k * 1.3), 0.3)
pop(A(0, 2, 0.5), 600); pop(A(0, 2, 0.7), 800)
creak(A(0, 3, 0.2), 1.0, 1.4); crackle(A(0, 3, 0.8), 0.6); splash(A(0, 3, 2.2), 1.2)
boom(E(0, 3, 0.2), 1.1); ding(E(0, 3, 0.35), 74, 1.2); ding(E(0, 3, 0.55), 81, 1.0)
# scene 1
pop(A(1, 0, 0.3), 600); sweep(A(1, 0, 1.4), 2.6, 200, 700, 0.5); bubbles(A(1, 0, 1.6), 10); pop(A(1, 0, 3.7), 800); ding(A(1, 0, 3.8), 76, 0.8)
pop(A(1, 1, 3.1), 600); pop(A(1, 1, 3.5), 900)
for k in range(6): knock(A(1, 1, 5.0 + k * 0.28), 0.5)
pop(A(1, 1, 6.8), 300, 2.0); boom(A(1, 1, 6.9), 0.7)
sweep(A(1, 1, 8.6), 2.6, 150, 600, 0.7); bubbles(A(1, 1, 8.8), 18); boom(A(1, 1, 10.5), 0.8); ding(A(1, 1, 10.6), 70, 0.9)
# scene 2
pop(A(2, 0, 0.2), 600); click(A(2, 0, 1.1), 1.2); pop(A(2, 0, 1.7), 800); ding(A(2, 0, 1.8), 79, 0.6)
sweep(A(2, 1, 0.2), 1.5, 200, 800, 0.5); bubbles(A(2, 1, 3.0), 14, 0.8)
for k in range(5): sweep(A(2, 1, 6.0 + k * 0.8), 0.6, 150, 400, 0.4)
pop(A(2, 1, 7.0), 800)
pop(A(2, 2, 0.6), 600); sweep(A(2, 2, 4.0), 3.6, 600, 150, 0.5); creak(A(2, 2, 4.5), 2.5)
pop(A(2, 2, 5.4), 700)
for k in range(60): knock(A(2, 3, 0.4 + k * 0.06), 0.25)
for k in range(40): tick(A(2, 3, 0.4 + k * 0.075), 0.3)
# scene 3
for k in range(3): pop(A(3, 0, 1.4 + k * 0.2), 600 + k * 120)
pop(A(3, 0, 3.0), 700); boom(A(3, 0, 4.8), 0.5)
for k in range(6): crackle(A(3, 1, 1.4 + k * 0.7), 0.25)
pop(A(3, 1, 3.0), 700); zap(A(3, 1, 6.2), 1200, 300, 0.5, 0.6); pop(A(3, 1, 6.6), 500)
pop(A(3, 2, 0.4), 600, 1.2); boom(A(3, 2, 0.5), 0.6)
crackle(A(3, 3, 0.5), 0.8); boom(A(3, 3, 0.6), 0.9); splash(A(3, 3, 1.5), 0.8); sweep(A(3, 3, 4.0), 1.0, 300, 2000, 0.6)
# scene 4
boom(A(4, 0, 0.6), 1.1); creak(A(4, 0, 0.4), 1.4, 1.3)
for k in range(5): pop(A(4, 1, 0.6 + k * 0.4), 500 + k * 100)
sweep(A(4, 1, 2.6), 1.0, 300, 900, 0.5)
sweep(A(4, 2, 0.6), 2.6, 150, 600, 0.6); bubbles(A(4, 2, 0.8), 12); pop(A(4, 2, 1.6), 800)
for k in range(40): tick(A(4, 2, 3.6 + k * 0.06), 0.4)
for k in range(100): pop(A(4, 3, 0.6 + k * 0.008), 900 + k * 4, 0.12)
for k in range(30): pop(A(4, 3, 4.6 + k * 0.11), 700 + k * 15, 0.25)
pop(A(4, 3, 6.0), 600); ding(A(4, 3, 6.1), 76, 0.8)
# scene 5
pop(A(5, 0, 1.4), 600); sweep(A(5, 0, 2.4), 0.6, 300, 1500, 0.5); pop(A(5, 0, 3.0), 800); ding(A(5, 0, 3.1), 79, 0.6)
pop(A(5, 0, 5.6), 700)
pop(A(5, 1, 0.4), 600)
for k in range(8): knock(A(5, 1, 0.8 + k * 0.2), 0.6)
pop(A(5, 1, 2.6), 800)
for k in range(10): knock(A(5, 1, 2.8 + k * 0.28), 0.3)
# scene 6
pop(A(6, 0, 0.6), 600, 1.2); bubbles(A(6, 0, 1.0), 8)
sweep(A(6, 1, 0.6), 2.0, 150, 900, 0.6); pop(A(6, 1, 1.0), 800); pop(A(6, 1, 2.4), 700); click(A(6, 1, 4.0), 1.0)
coins(A(6, 2, 0.6), 18); boom(A(6, 2, 0.7), 0.7); pop(A(6, 2, 3.0), 800); coins(A(6, 2, 3.1), 6)
for k in range(3): pop(A(6, 3, 0.8 + k * 1.1), 500 + k * 150)
pop(A(6, 3, 5.6), 800); ding(A(6, 3, 5.7), 79, 0.7)
# scene 7
sweep(A(7, 0, 0.4), 5.0, 150, 500, 0.4); bubbles(A(7, 0, 0.8), 16, 0.7); pop(A(7, 0, 5.0), 700)
for k in range(5): pop(A(7, 0, 6.2 + k * 0.3), 1000 + k * 100, 0.5)
pop(A(7, 1, 1.6), 600); ding(A(7, 1, 1.7), 76, 0.6)
for k in range(31): tick(A(7, 1, 3.8 + k * 0.05), 0.4)
pop(A(7, 2, 0.6), 600); sweep(A(7, 2, 1.0), 2.0, 900, 300, 0.4); pop(A(7, 2, 2.6), 800); knock(A(7, 2, 3.0), 0.8)
boom(A(7, 3, 0.4), 0.8); ding(A(7, 3, 2.0), 72, 1.0)
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
