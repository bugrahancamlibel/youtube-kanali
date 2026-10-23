"""Cloud voice-over: projects/<slug>/ElevenLabs Metni.txt -> out/vo.mp3 via the ElevenLabs API.

Runs in GitHub Actions (workflow "Seslendirme"), so the API key stays a repository secret.
Env: PROJECT (slug), ELEVENLABS_API_KEY, optional ELEVENLABS_VOICE_ID, optional ELEVENLABS_MODEL (default eleven_v4)
Exit codes: 2 = not enough credits, 3 = voice not found, 4 = other API error.
"""
import json, os, sys
import requests

API = 'https://api.elevenlabs.io'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def die(code, msg):
    print(f'::error::{msg}'); sys.exit(code)


def main():
    slug = os.environ['PROJECT'].strip()
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key:
        die(4, 'ELEVENLABS_API_KEY secret ayarlı değil (Settings > Secrets and variables > Actions).')
    text = open(os.path.join(ROOT, 'projects', slug, 'ElevenLabs Metni.txt'), encoding='utf-8').read().strip()
    H = {'xi-api-key': key}
    sub = requests.get(f'{API}/v1/user/subscription', headers=H, timeout=60)
    if sub.status_code == 200:
        s = sub.json()
        left = s.get('character_limit', 0) - s.get('character_count', 0)
        print(f"kredi: kalan {left}, gereken ~{len(text)} (plan: {s.get('tier')})")
        if left < len(text):
            die(2, f'ElevenLabs kredisi yetersiz: kalan {left}, gereken {len(text)}.')
    else:
        print('::warning::kredi okunamadı', sub.status_code, sub.text[:200])
    vid = os.environ.get('ELEVENLABS_VOICE_ID', '').strip()
    if not vid:
        r = requests.get(f'{API}/v2/voices', headers=H, params={'search': 'Max', 'page_size': 100}, timeout=60)
        voices = r.json().get('voices', []) if r.status_code == 200 else []
        cand = [v for v in voices if v.get('name', '').lower().startswith('max')]
        cand.sort(key=lambda v: ('documentary' not in v.get('name', '').lower(), 'elearning' not in v.get('name', '').lower()))
        if not cand:
            die(3, '"Max - Elearning and Documentary" sesi hesabında bulunamadı. ElevenLabs > Voices > bu sesi '
                   '"My Voices"a ekle ya da voice ID\'yi ELEVENLABS_VOICE_ID repo değişkeni olarak gir.')
        vid = cand[0]['voice_id']
        print('ses:', cand[0]['name'], vid)
    models = [os.environ.get('ELEVENLABS_MODEL') or 'eleven_v4', 'eleven_v3']
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    for model in models:
        r = requests.post(f'{API}/v1/text-to-speech/{vid}', headers={**H, 'Content-Type': 'application/json'},
                          params={'output_format': 'mp3_44100_128'}, json={'text': text, 'model_id': model}, timeout=600)
        if r.status_code == 200 and r.headers.get('content-type', '').startswith('audio'):
            open(os.path.join(ROOT, 'out', 'vo.mp3'), 'wb').write(r.content)
            json.dump({'project': slug, 'model': model, 'voice_id': vid, 'chars': len(text)},
                      open(os.path.join(ROOT, 'out', 'vo.json'), 'w'))
            print(f'ok: {len(r.content)} bayt, model {model}')
            return
        print(f'::warning::model {model} başarısız: HTTP {r.status_code} {r.text[:300]}')
        if r.status_code in (401, 402) or 'quota' in r.text.lower():
            die(2, f'ElevenLabs reddetti (HTTP {r.status_code}): {r.text[:300]}')
    die(4, 'Seslendirme üretilemedi.')


if __name__ == '__main__':
    main()
