"""Cut both Shorts of a project from its finished (voiced) long video, using <project>/shorts_plan.json.

usage: python3 tools/shorts_from_plan.py <project_dir> <long_video.mp4> [out_dir]

shorts_plan.json:
{
  "HL": {"1": 0.34, ...},                       # transition half-lengths from main.py TRANS
  "shorts": [
    {"out": "Short 1 - Title.mp4",
     "first": [0, 0], "last": [0, 3],            # (scene, line) of the first and the LAST (payoff) line
     "tail": 2.0,                                # seconds kept after the payoff line (title card etc.)
     "hook": [[["TEXT", "#fff"]], ...], "hook2": [...], "hook2_line": [0, 3],
     "freeze": -0.3}                             # freeze frame for the end card: seconds relative to the segment end
  ]
}
Rules (why this exists): a Short must END right after its payoff line, never bleed into the next line or a
scene transition, then hold a frozen hero frame with the "WATCH THE FULL VIDEO" end card.
Needs vo/warp.json and captions_real.json in the project (made during the voice sync step).
"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from short_plan import segment, _load

proj, video = sys.argv[1], sys.argv[2]
out_dir = sys.argv[3] if len(sys.argv) > 3 else proj
plan = json.load(open(os.path.join(proj, 'shorts_plan.json')))
HL = {int(k): v for k, v in plan['HL'].items()}
m, S, LN, Wf = _load(proj)
caps = json.load(open(os.path.join(proj, 'captions_real.json')))
caps = [c[:3] for c in caps]
for sh in plan['shorts']:
    start, end = segment(proj, tuple(sh['first']), tuple(sh['last']), HL, tail=sh.get('tail', 0.7))
    spec = {'video': video, 'out': os.path.join(out_dir, sh['out']), 'start': start, 'end': end,
            'hook': sh['hook'], 'captions': caps, 'footer': sh.get('footer', 'Full video on the channel'),
            'end_hold': sh.get('end_hold', 1.8), 'freeze_at': round(end + sh.get('freeze', -0.3), 3)}
    if sh.get('hook2'):
        si, li = sh['hook2_line']
        spec['hook2'] = sh['hook2']
        spec['hook_until'] = round(Wf(S[si] + LN[si][li][0]) - start, 2)
    sp = os.path.join(proj, 'spec_' + os.path.splitext(os.path.basename(sh['out']))[0].replace(' ', '_') + '.json')
    json.dump(spec, open(sp, 'w'), indent=1)
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_short.py'), sp], check=True)
    print(f"{sh['out']}: {start:.2f} -> {end:.2f}  ({end - start + spec['end_hold']:.1f} s with end card)")
