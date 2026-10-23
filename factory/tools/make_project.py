"""Write projects/<slug>/project.json (read by the cloud publisher in publisher/publish.py).

python3 factory/tools/make_project.py spec.json
spec.json = {
  "slug": "06-some-topic", "number": "06", "name": "Some Topic", "factory_dir": "sometopic",
  "tags": ["WhatIf", "Space"],
  "long":   {"title": "...", "description": "... chapters ... sources ... Narration: AI voice (ElevenLabs)."},
  "shorts": [{"title": "...", "description": "one-line teaser. Full video on the channel."},
             {"title": "...", "description": "..."}],
  "status": "ready"            # or "needs_voice"
}
Publish dates are NOT set here: the publisher gives them when the project is approved (issue comment "onay").
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def build(p):
    tg = ' '.join('#' + t for t in p.get('tags', []))
    ups = []
    for i, s in enumerate(p['shorts'], 1):
        title = s['title'] if '#shorts' in s['title'].lower() else s['title'][:90] + ' #Shorts'
        ups.append({'id': f'short{i}', 'type': 'short', 'asset': f'short{i}.mp4', 'title': title,
                    'caption': f"{title.replace(' #Shorts', '')} {tg} #Shorts".strip(),
                    'description': f"{s['description']}\n\n{tg} #Shorts".strip(), 'tags': p.get('tags', []),
                    'state': 'planned', 'attempts': 0})
    L = p['long']
    ups.insert(1, {'id': 'long', 'type': 'long', 'asset': 'long.mp4', 'title': L['title'][:100], 'caption': L['title'],
                   'description': f"{L['description']}\n\n{tg}".strip(), 'tags': p.get('tags', []), 'state': 'planned', 'attempts': 0})
    return {'slug': p['slug'], 'number': p['number'], 'name': p['name'], 'videos': f"videolar:{p['slug']}/",
            'approved': False, 'status': p.get('status', 'ready'), 'factory_dir': p.get('factory_dir', ''), 'uploads': ups}


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = os.path.join(ROOT, 'projects', spec['slug'], 'project.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    old = json.load(open(out, encoding='utf-8')) if os.path.exists(out) else None
    d = build(spec)
    if old:                                   # keep approval / state info of an existing project
        for k in ('approved', 'approved_note'):
            if k in old: d[k] = old[k]
    json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('wrote', out)
