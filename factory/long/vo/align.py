import sys, re, numpy as np
from scipy.io import wavfile
sys.path.insert(0, '.')
from script import SCRIPT
LINES = [l for sc in SCRIPT for l in sc]
def syl(txt):
    txt = txt.lower().replace('2014', 'twenty fourteen').replace('2017', 'twenty seventeen').replace('2024', 'twenty twenty four') \
        .replace('2025', 'twenty twenty five').replace('2026', 'twenty twenty six').replace('2027', 'twenty twenty seven') \
        .replace('48', 'forty eight').replace('cfo', 'see eff oh').replace(' ai', ' ay eye').replace('us ', 'you ess ')
    n = 0
    for w in re.findall(r"[a-z']+", txt):
        k = len(re.findall(r'[aeiouy]+', w))
        if w.endswith('e') and k > 1 and not w.endswith('le'): k -= 1
        n += max(1, k)
    return n
SYL = [syl(l) for l in LINES]
sr, x = wavfile.read(sys.argv[1]); x = x.astype(float) / 32768
hop = int(sr * 0.01)
e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
db = 20 * np.log10(e + 1e-9); v = db > np.percentile(db, 99) - 38
segs = []; i = 0; n = len(v)
while i < n:
    if v[i]:
        j = i
        while j < n and (v[j] or (j + 18 < n and v[j:j + 18].any())): j += 1
        segs.append((i / 100, j / 100)); i = j
    else: i += 1
segs = [s for s in segs if s[1] - s[0] > 0.06]
M = len(segs); K = len(LINES)
print(len(x) / sr, 's', M, 'segments', K, 'lines')
dur = lambda a, b: segs[b - 1][1] - segs[a][0]
best = None
for rate in np.linspace(0.12, 0.26, 57):
    INF = 1e9
    D = np.full((K + 1, M + 1), INF); P = np.zeros((K + 1, M + 1), int); D[0][0] = 0
    for k in range(1, K + 1):
        for m in range(1, M + 1):
            for a in range(max(0, m - 12), m):
                if D[k - 1][a] >= INF: continue
                c = (dur(a, m) - rate * SYL[k - 1]) ** 2 / max(1, rate * SYL[k - 1])
                gap = (segs[m][0] - segs[m - 1][1]) if m < M else 1.0
                c -= 1.2 * gap
                if D[k - 1][a] + c < D[k][m]: D[k][m] = D[k - 1][a] + c; P[k][m] = a
    if best is None or D[K][M] < best[0]: best = (D[K][M], rate, P.copy())
_, rate, P = best
bounds = []; m = M
for k in range(K, 0, -1):
    a = P[k][m]; gap_after = (segs[m][0] - segs[m - 1][1]) if m < M else 9
    bounds.append((segs[a][0], segs[m - 1][1], gap_after)); m = a
bounds = bounds[::-1]
print('rate', round(rate, 3))
for (a, b, g), L_, s in zip(bounds, LINES, SYL):
    print(f'{a:7.2f}-{b:7.2f} {b-a:5.2f}s exp {rate*s:5.2f} gap {g:4.2f} | {L_[:60]}')
np.save(sys.argv[1] + '.bounds.npy', np.array([(a, b) for a, b, g in bounds]))
