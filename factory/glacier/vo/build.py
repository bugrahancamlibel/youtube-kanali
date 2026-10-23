import sys, json, numpy as np
from scipy.io import wavfile
sys.path.insert(0, '.')
from script import SCRIPT, timeline
S, LN = timeline()
HL = {1: .42, 2: .34, 3: .36, 4: .45, 5: .34, 6: .36, 7: .6}
SR = 44100
sr, x = wavfile.read('vo/g1.wav'); x = x.astype(float) / 32768
B = np.load('vo/g1.wav.bounds.npy')
lines = []   # (scene, design_start, design_end, clip)
k = 0
for si, sc in enumerate(SCRIPT):
    for li in range(len(sc)):
        a, b = B[k]
        s0 = max(0, int((a - 0.04) * SR)); s1 = min(len(x), int((b + 0.12) * SR))
        clip = x[s0:s1].copy(); f = int(0.01 * SR); clip[:f] *= np.linspace(0, 1, f); clip[-f * 4:] *= np.linspace(1, 0, f * 4)
        take_gap = (B[k + 1][0] - b) if k + 1 < len(B) else 0.6
        lines.append((si, S[si] + LN[si][li][0], S[si] + LN[si][li][1], clip, take_gap)); k += 1
pairs = [(0.0, 0.0)]; starts = []; ends = []
prev_si = 0
for i, (si, ds, de, clip, tg) in enumerate(lines):
    d = len(clip) / SR
    if i == 0:
        t = ds
    elif si != prev_si:
        hl = HL[si]
        pde, pre = lines[i - 1][2], ends[-1]
        t_tr0 = pre + max(0.35, (S[si] - hl) - pde)
        pairs += [(S[si] - hl, t_tr0), (S[si] + hl, t_tr0 + 2 * hl)]
        ds = max(ds, S[si] + hl + 0.05)
        t = t_tr0 + 2 * hl + (ds - (S[si] + hl))
    else:
        t = ends[-1] + min(0.8, max(0.35, lines[i - 1][4]))
    pairs += [(ds, t), (de, t + d)]
    starts.append(t); ends.append(t + d); prev_si = si
total = ends[-1] + (S[-1] - lines[-1][2])
pairs.append((S[-1], total))
# sanity: monotone
for (a0, b0), (a1, b1) in zip(pairs, pairs[1:]):
    assert a1 > a0 and b1 > b0, (a0, b0, a1, b1)
out = np.zeros(int(total * SR) + SR)
for t, l in zip(starts, lines):
    i0 = int(t * SR); out[i0:i0 + len(l[3])] += l[3]
out = out[:int(total * SR)]
out = out / np.max(np.abs(out)) * 0.85
wavfile.write('vo/vo_track.wav', SR, (out * 32767).astype(np.int16))
json.dump({'pairs': pairs, 'total': total}, open('vo/warp.json', 'w'))
print('total', round(total, 2), 'pairs', len(pairs))
for si in range(8):
    print(si, 'design', round(S[si], 1), '->', round(float(np.interp(S[si], [p[0] for p in pairs], [p[1] for p in pairs])), 1))
