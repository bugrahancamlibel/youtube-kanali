"""Cloud publisher for the YouTube channel (runs in GitHub Actions, no local computer needed).

Every run:
  1. gives publish dates to approved projects that have none (cadence: Short 1, long video next day,
     Short 2 two days after that; next project starts two days after the previous Short 2; 20:30 local),
  2. if the plan has fallen behind (e.g. setup took a few days) shifts all unsent items by whole days,
     so the order and the spacing stay the same and nothing is published in a burst,
  3. sends the items that are due to Upload-Post (mode "just_in_time"), or schedules every future item on
     Upload-Post right away (mode "schedule_ahead", needs a paid Upload-Post plan),
  4. checks the status of earlier async uploads, writes everything back to projects/*/project.json and
     regenerates YAYIN_TAKVIMI.md. Problems are reported as GitHub issues.

Env: UPLOAD_POST_API_KEY (secret), GH_TOKEN + GITHUB_REPOSITORY (from Actions), DRY_RUN=1 to only print,
     NOW=<iso> to simulate a time (tests), UPLOAD_POST_BASE to point at a mock server (tests).
"""
import glob, json, math, os, re, subprocess, sys, tempfile, time
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get('UPLOAD_POST_BASE', 'https://api.upload-post.com')
ORDER = {'short1': 0, 'long': 1, 'short2': 2}
GUN = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']


def fmt_local(s, cfg):
    d = pt(s).astimezone(tz_of(cfg))
    return f"{d.strftime('%d.%m.%Y')} {GUN[d.weekday()]} {d.strftime('%H:%M')}"


def log(*a):
    print(*a, flush=True)


def now_utc():
    v = os.environ.get('NOW')
    return datetime.fromisoformat(v).astimezone(timezone.utc) if v else datetime.now(timezone.utc)


def load_config():
    cfg = json.load(open(os.path.join(ROOT, 'config.json'), encoding='utf-8'))
    cfg.setdefault('mode', 'just_in_time')
    cfg.setdefault('publish_time', '20:30')
    cfg.setdefault('utc_offset', '+03:00')
    cfg.setdefault('max_per_run', 2)
    cfg.setdefault('late_shift_hours', 6)
    return cfg


def tz_of(cfg):
    sign = 1 if cfg['utc_offset'][0] == '+' else -1
    h, m = map(int, cfg['utc_offset'][1:].split(':'))
    return timezone(sign * timedelta(hours=h, minutes=m))


def load_projects():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'projects', '*', 'project.json'))):
        d = json.load(open(p, encoding='utf-8'))
        d['_path'] = p
        out.append(d)
    return out


def save_project(d):
    p = d.pop('_path')
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(p, 'a').write('\n')
    d['_path'] = p


def pt(s):
    return datetime.fromisoformat(s)


def iso_local(dt, cfg):
    return dt.astimezone(tz_of(cfg)).isoformat(timespec='seconds')


def unsent(u):
    return u.get('state', 'planned') in ('planned', 'retry')


# ------------------------------------------------------------------ planning
def assign_dates(projects, cfg, now):
    """Give dates to approved projects without a full plan. Returns list of changed slugs."""
    changed = []
    tz = tz_of(cfg)
    hh, mm = map(int, cfg['publish_time'].split(':'))
    dated = [pt(u['publish_at']) for p in projects if p.get('approved') for u in p['uploads'] if u.get('publish_at')]
    for p in projects:
        if not p.get('approved') or p.get('status') != 'ready':
            continue
        if all(u.get('publish_at') for u in p['uploads']):
            continue
        if dated:
            d0 = (max(dated).astimezone(tz) + timedelta(days=2)).date()
        else:
            loc = now.astimezone(tz)
            today_slot = datetime(loc.year, loc.month, loc.day, hh, mm, tzinfo=tz)
            d0 = loc.date() if today_slot - loc > timedelta(hours=3) else loc.date() + timedelta(days=1)
        offs = {'short1': 0, 'long': 1, 'short2': 3}
        for u in p['uploads']:
            if not u.get('publish_at'):
                day = d0 + timedelta(days=offs.get(u['id'], 0))
                u['publish_at'] = datetime(day.year, day.month, day.day, hh, mm, tzinfo=tz).isoformat(timespec='seconds')
                dated.append(pt(u['publish_at']))
        changed.append(p['slug'])
    return changed


def shift_if_late(projects, cfg, now):
    """If the earliest unsent item is more than late_shift_hours late, move every unsent item of every approved
    project forward by the same number of whole days (keeps order and spacing)."""
    items = [(pt(u['publish_at']), p, u) for p in projects if p.get('approved') and p.get('status') == 'ready'
             for u in p['uploads'] if unsent(u) and u.get('publish_at')]
    if not items:
        return 0
    earliest = min(i[0] for i in items)
    late = now - earliest
    if late <= timedelta(hours=cfg['late_shift_hours']):
        return 0
    days = math.ceil((late - timedelta(hours=cfg['late_shift_hours'])) / timedelta(days=1))
    # land on the first slot that is still ahead (or within the grace window)
    while earliest + timedelta(days=days) < now - timedelta(hours=cfg['late_shift_hours']):
        days += 1
    for _, p, u in items:
        u['publish_at'] = (pt(u['publish_at']) + timedelta(days=days)).isoformat(timespec='seconds')
        u.setdefault('notes', []).append(f'{now.date()}: {days} gün ileri kaydırıldı (plan gecikmişti)')
    return days


# ------------------------------------------------------------------ github helpers
def gh(*args, check=True):
    return subprocess.run(['gh', *args], capture_output=True, text=True, check=check)


def download_asset(project, asset, dest, cfg=None):
    """Videos live on the `videolar` branch: <slug>/<asset> (GitHub contents API, files up to 100 MB)."""
    if os.environ.get('LOCAL_ASSET_DIR'):            # tests
        return os.path.join(os.environ['LOCAL_ASSET_DIR'], asset)
    branch = (cfg or {}).get('video_branch', 'videolar')
    repo = os.environ.get('GITHUB_REPOSITORY', 'bugrahancamlibel/youtube-kanali')
    path = os.path.join(dest, asset)
    with open(path, 'wb') as fh:
        r = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github.raw',
                            f"/repos/{repo}/contents/{project['slug']}/{asset}?ref={branch}"], stdout=fh, stderr=subprocess.PIPE)
    if r.returncode != 0 or os.path.getsize(path) < 10000:
        raise RuntimeError(f"video indirilemedi: {branch}:{project['slug']}/{asset}: {r.stderr.decode()[:300]}")
    return path


def report_issue(title, body):
    if os.environ.get('DRY_RUN') == '1' or not os.environ.get('GITHUB_REPOSITORY'):
        log('ISSUE (not created):', title, '\n', body)
        return
    r = gh('issue', 'list', '--state', 'open', '--search', f'"{title}" in:title', '--json', 'number', check=False)
    try:
        if json.loads(r.stdout or '[]'):
            return
    except ValueError:
        pass
    gh('label', 'create', 'yayin-hatasi', '--color', 'd73a4a', '--force', check=False)
    gh('issue', 'create', '--title', title, '--body', body, '--label', 'yayin-hatasi', check=False)


# ------------------------------------------------------------------ upload-post
def form_fields(cfg, project, u, platforms, scheduled_utc=None):
    f = [('user', cfg['upload_post_user'])]
    f += [('platform[]', x) for x in platforms]
    f += [('title', u['title']), ('description', u['description']), ('async_upload', 'true'),
          ('external_id', f"{project['slug']}/{u['id']}")]
    if 'youtube' in platforms:
        f += [('categoryId', str(cfg.get('youtube_category', '28'))), ('privacyStatus', 'public'),
              ('containsSyntheticMedia', 'false'), ('selfDeclaredMadeForKids', 'false')]
        for tag in u.get('tags', []):
            f.append(('tags[]', tag))
    ai = 'true' if cfg.get('ai_label', True) else 'false'
    if 'tiktok' in platforms:
        f += [('tiktok_title', u.get('caption', u['title'])), ('is_aigc', ai)]
    if 'instagram' in platforms:
        f += [('instagram_title', u.get('caption', u['title'])), ('is_ai_generated', ai)]
    if 'facebook' in platforms:
        f += [('facebook_title', u['title']), ('facebook_description', u['description']), ('facebook_is_ai_generated', ai)]
        if cfg.get('facebook_page_id'):
            f.append(('facebook_page_id', str(cfg['facebook_page_id'])))
    if scheduled_utc:
        f += [('scheduled_date', scheduled_utc), ('timezone', 'UTC')]
    return f


def post_upload(cfg, key, project, u, video_path, platforms, scheduled_utc=None):
    import requests
    idem = re.sub(r'[^A-Za-z0-9-]', '', f"{project['slug']}-{u['id']}-a{u.get('attempts', 0)}-{'-'.join(sorted(platforms))}")
    with open(video_path, 'rb') as fh:
        files = {'video': (os.path.basename(video_path), fh, 'video/mp4')}
        r = requests.post(f'{BASE}/api/upload', data=form_fields(cfg, project, u, platforms, scheduled_utc),
                          files=files, headers={'Authorization': f'Apikey {key}', 'Idempotency-Key': idem}, timeout=600)
    try:
        body = r.json()
    except ValueError:
        body = {'raw': r.text[:500]}
    return r.status_code, body


def check_status(key, request_id):
    import requests
    r = requests.get(f'{BASE}/api/uploadposts/status', params={'request_id': request_id},
                     headers={'Authorization': f'Apikey {key}'}, timeout=60)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, {'raw': r.text[:500]}


def platform_errors(results):
    errs = {}
    if isinstance(results, dict):
        for k, v in results.items():
            if isinstance(v, dict) and v.get('success') is False and not v.get('skipped'):
                errs[k] = v.get('error') or v.get('message') or 'hata'
    return errs


def send_one(cfg, key, project, u, now, scheduled_utc=None):
    platforms = list(u.get('platforms') or (cfg['short_platforms'] if u['type'] == 'short' else cfg['long_platforms']))
    with tempfile.TemporaryDirectory() as tmp:
        path = download_asset(project, u['asset'], tmp, cfg)
        code, body = post_upload(cfg, key, project, u, path, platforms, scheduled_utc)
        if code == 403 and 'tiktok' in platforms:
            log('  TikTok bu planda izinli değil, TikTok olmadan tekrar deneniyor')
            platforms = [x for x in platforms if x != 'tiktok']
            u.setdefault('notes', []).append(f'{now.date()}: TikTok çıkarıldı (Upload-Post planı izin vermedi)')
            code, body = post_upload(cfg, key, project, u, path, platforms, scheduled_utc)
    u['attempts'] = u.get('attempts', 0) + 1
    ok = code in (200, 202) and body.get('success') is not False
    if ok:
        u['state'] = 'scheduled' if scheduled_utc else 'sent'
        u['sent_at'] = iso_local(now, cfg)
        u['sent_platforms'] = platforms
        for k in ('request_id', 'job_id', 'scheduled_date'):
            if body.get(k): u[k] = body[k]
        if body.get('results'):
            u['results'] = body['results']
            errs = platform_errors(body['results'])
            if errs: u['platform_errors'] = errs
        u.pop('last_error', None)
        return True, body
    u['last_error'] = f'HTTP {code}: ' + json.dumps(body, ensure_ascii=False)[:600]
    u['state'] = 'retry' if u['attempts'] < 3 else 'failed'
    return False, body


# ------------------------------------------------------------------ calendar file
def write_calendar(projects, cfg):
    rows = []
    for p in projects:
        for u in p['uploads']:
            rows.append((u.get('publish_at') or '9999', p, u))
    rows.sort(key=lambda r: r[0])
    st = {'planned': 'planlandı', 'retry': 'tekrar denenecek', 'sent': 'gönderildi', 'scheduled': "Upload-Post'ta planlı",
          'failed': 'HATA', 'published': 'yayında'}
    out = ['# Yayın takvimi', '', 'Bu dosya her çalışmada otomatik güncellenir. Saatler Türkiye saati.', '',
           '| Tarih | Proje | İçerik | Platformlar | Durum |', '|---|---|---|---|---|']
    for when, p, u in rows:
        if not p.get('approved'):
            continue
        d = fmt_local(u['publish_at'], cfg) if u.get('publish_at') else '-'
        plats = ', '.join(u.get('sent_platforms') or u.get('platforms') or
                          (cfg['short_platforms'] if u['type'] == 'short' else cfg['long_platforms']))
        title = u['title'].replace('|', '\\|')
        out.append(f"| {d} | {p['number']} - {p['name']} | {title} | {plats} | {st.get(u.get('state', 'planned'), u.get('state'))} |")
    waiting = [p for p in projects if not p.get('approved')]
    if waiting:
        out += ['', '## Onay / ses bekleyenler', '']
        for p in waiting:
            out.append(f"- {p['number']} - {p['name']}: {'ses bekliyor' if p.get('status') == 'needs_voice' else 'onay bekliyor'}")
    open(os.path.join(ROOT, 'YAYIN_TAKVIMI.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')


# ------------------------------------------------------------------ main
def main():
    cfg = load_config()
    now = now_utc()
    projects = load_projects()
    key = os.environ.get('UPLOAD_POST_API_KEY', '').strip()
    dry = os.environ.get('DRY_RUN') == '1'
    ready = bool(key) and cfg.get('upload_post_user') not in (None, '', 'KULLANICI_ADINI_YAZ')
    if not ready and not dry:
        log('::warning::UPLOAD_POST_API_KEY secret veya config.json içindeki upload_post_user henüz ayarlı değil. '
            'Bu çalışmada hiçbir şey gönderilmedi (sadece takvim güncellendi).')

    assigned = assign_dates(projects, cfg, now)
    if assigned: log('tarih verildi:', ', '.join(assigned))
    shifted = shift_if_late(projects, cfg, now)
    if shifted: log(f'plan gecikmişti, kalan her şey {shifted} gün ileri alındı')

    sent = 0
    if ready and not dry:
        # follow up async uploads
        for p in projects:
            for u in p['uploads']:
                if u.get('state') == 'sent' and u.get('request_id') and not u.get('final'):
                    code, body = check_status(key, u['request_id'])
                    if code == 200 and isinstance(body, dict):
                        res = body.get('results') or body.get('result')
                        status = str(body.get('status', '')).lower()
                        if res: u['results'] = res
                        errs = platform_errors(res)
                        if errs: u['platform_errors'] = errs
                        if status in ('completed', 'success', 'finished', 'done', 'failed', 'error') or res:
                            u['final'] = True
                            if errs:
                                report_issue(f"Yayın hatası: {p['number']} {u['id']}",
                                             f"`{p['slug']}` / `{u['id']}` bazı platformlarda yayınlanamadı:\n\n```\n"
                                             f"{json.dumps(errs, ensure_ascii=False, indent=1)}\n```\n"
                                             "Tekrar denemek için project.json'da bu öğenin `state` alanını `retry` yap.")
        # send what is due / schedule ahead
        queue = sorted([(pt(u['publish_at']), p, u) for p in projects if p.get('approved') and p.get('status') == 'ready'
                        for u in p['uploads'] if unsent(u) and u.get('publish_at')], key=lambda x: x[0])
        for when, p, u in queue:
            if sent >= cfg['max_per_run']:
                break
            due = when <= now + timedelta(minutes=5)
            sched = None
            if not due:
                if cfg['mode'] != 'schedule_ahead' or when > now + timedelta(days=360):
                    continue
                sched = when.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            log(f"gönderiliyor: {p['slug']} / {u['id']} ({'planlı ' + sched if sched else 'hemen'})")
            try:
                ok, body = send_one(cfg, key, p, u, now, sched)
            except Exception as e:                     # network, missing asset ...
                u['attempts'] = u.get('attempts', 0) + 1
                u['last_error'] = str(e)[:600]
                u['state'] = 'retry' if u['attempts'] < 3 else 'failed'
                ok, body = False, {'error': str(e)}
            sent += 1
            log('  sonuç:', 'OK' if ok else 'HATA', json.dumps(body, ensure_ascii=False)[:400])
            if not ok and u['state'] == 'failed':
                report_issue(f"Yayın hatası: {p['number']} {u['id']}",
                             f"`{p['slug']}` / `{u['id']}` 3 denemede gönderilemedi.\n\nSon hata:\n```\n{u['last_error']}\n```\n"
                             "Sorunu düzeltince project.json'da `state` alanını `retry`, `attempts` alanını 0 yap.")
    else:
        due = [(p['slug'], u['id'], u['publish_at']) for p in projects if p.get('approved') and p.get('status') == 'ready'
               for u in p['uploads'] if unsent(u) and u.get('publish_at') and pt(u['publish_at']) <= now + timedelta(minutes=5)]
        log('DRY/hazır değil - şu an sırası gelenler:', due)

    for p in projects:
        save_project(p)
    write_calendar(projects, cfg)
    log(f'bitti: {sent} gönderim')


if __name__ == '__main__':
    main()
