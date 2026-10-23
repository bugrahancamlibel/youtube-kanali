"""Compute clean Short boundaries from a synced long video.

A Short must START just before a line begins and END right after a payoff line finishes:
never bleed into the next line, never run into a scene transition. make_short.py then adds an end card.

usage (python):  from short_plan import segment
    start, end = segment(project_dir, (scene, line), (scene, line), HL)
"""
import json, os, sys, importlib.util
import numpy as np


def _load(project_dir):
    spec = importlib.util.spec_from_file_location('proj_script', os.path.join(project_dir, 'script.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    S, LN = m.timeline()
    wj = json.load(open(os.path.join(project_dir, 'vo', 'warp.json')))
    D = [p[0] for p in wj['pairs']]; R = [p[1] for p in wj['pairs']]
    W = lambda x: float(np.interp(x, D, R))
    return m, S, LN, W


def segment(project_dir, first, last, HL, lead=0.35, tail=0.7):
    m, S, LN, W = _load(project_dir)
    fs, fl = first; ls_, ll = last
    a = W(S[fs] + LN[fs][fl][0])
    b = W(S[ls_] + LN[ls_][ll][1])
    # previous line end (do not include its tail)
    prev_end = None
    if fl > 0: prev_end = W(S[fs] + LN[fs][fl - 1][1])
    elif fs > 0: prev_end = W(S[fs] + HL.get(fs, 0.4))      # transition into this scene
    start = a - lead if prev_end is None else max(a - lead, prev_end + 0.08)
    # limit for the end: next line start, or the next scene's transition start
    if ll + 1 < len(LN[ls_]):
        limit = W(S[ls_] + LN[ls_][ll + 1][0]) - 0.12
    else:
        nb = ls_ + 1
        limit = W(S[nb] - HL.get(nb, 0.4)) - 0.05 if nb < len(S) - 1 else W(S[-1])
    end = min(b + tail, limit)
    return round(max(0.0, start), 3), round(end, 3)


if __name__ == '__main__':
    d = sys.argv[1]
    print(segment(d, tuple(map(int, sys.argv[2].split(','))), tuple(map(int, sys.argv[3].split(','))), {}))
