"""Handles an approval comment on a "[Onay]" issue (runs in GitHub Actions, see .github/workflows/onay.yml).

The issue body contains a marker  <!-- project: 06-some-slug -->.
Comment "onay" (or onayla, /onay, evet, ok, approve)  -> project approved, dates assigned, issue closed.
Comment "ret"  (or reddet, iptal, /ret, no, reject)   -> project rejected, issue closed.
Anything else is ignored.
Env: COMMENT, ISSUE_BODY, ISSUE_NUMBER, GH_TOKEN, GITHUB_REPOSITORY
"""
import json, os, re, subprocess, sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish as P

YES = {'onay', 'onayla', 'onaylıyorum', 'onayliyorum', '/onay', 'evet', 'ok', 'tamam', 'approve', 'yayınla', 'yayinla'}
NO = {'ret', 'reddet', 'iptal', '/ret', 'hayır', 'hayir', 'no', 'reject'}


def comment(num, text):
    if os.environ.get('GITHUB_REPOSITORY'):
        subprocess.run(['gh', 'issue', 'comment', str(num), '--body', text], check=False)
    else:
        print('COMMENT:', text)


def close(num, label):
    if os.environ.get('GITHUB_REPOSITORY'):
        subprocess.run(['gh', 'label', 'create', label, '--color', '0e8a16', '--force'], check=False)
        subprocess.run(['gh', 'issue', 'edit', str(num), '--add-label', label, '--remove-label', 'onay-bekliyor'], check=False)
        subprocess.run(['gh', 'issue', 'close', str(num)], check=False)


def main():
    text = (os.environ.get('COMMENT') or '').strip().lower()
    word = re.split(r'[\s.!,]+', text)[0] if text else ''
    m = re.search(r'<!--\s*project:\s*([\w.-]+)\s*-->', os.environ.get('ISSUE_BODY') or '')
    num = os.environ.get('ISSUE_NUMBER', '0')
    if not m or (word not in YES and word not in NO):
        print('onay/ret yorumu değil, geçiliyor'); return
    slug = m.group(1)
    cfg = P.load_config()
    projects = P.load_projects()
    proj = next((p for p in projects if p['slug'] == slug), None)
    if not proj:
        comment(num, f'`{slug}` projesi depoda bulunamadı.'); return
    if word in NO:
        proj['approved'] = False
        proj['status'] = 'rejected'
        P.save_project(proj)
        comment(num, 'Tamam, bu proje yayınlanmayacak (reddedildi).')
        close(num, 'reddedildi'); return
    if proj.get('status') != 'ready':
        comment(num, f"Bu proje henüz yayına hazır değil (durum: `{proj.get('status')}`). Hazır olunca tekrar onay istenecek.")
        return
    proj['approved'] = True
    P.assign_dates(projects, cfg, P.now_utc())
    for p in projects:
        P.save_project(p)
    P.write_calendar(projects, cfg)
    lines = [f"- **{u['id']}** · {P.fmt_local(u['publish_at'], cfg)} · {u['title']}"
             for u in sorted(proj['uploads'], key=lambda u: u['publish_at'])]
    comment(num, 'Onaylandı, takvime alındı:\n\n' + '\n'.join(lines) +
            '\n\nTüm takvim: `YAYIN_TAKVIMI.md`. Plan kayarsa sıra ve aralıklar korunarak ileri alınır.')
    close(num, 'onaylandi')


if __name__ == '__main__':
    main()
