/**
 * YouTube Yayın Paneli — Google Apps Script (bir Google E-Tablosuna bağlı çalışır)
 *
 * Bilgisayar kapalıyken de Google'ın sunucularında çalışır:
 *  - Her 15 dakikada: onaylı videolardan sırası geleni Upload-Post ile YouTube / TikTok / Instagram / Facebook'a gönderir.
 *  - Saatte bir: GitHub'daki projeleri (bugrahancamlibel/youtube-kanali) tabloya alır, sesi bekleyen projeyi
 *    ElevenLabs ile seslendirip GitHub'a koyar, eski yayınların sonucunu kontrol eder.
 *  - Onay: "Projeler" sayfasında "Onay" kutusunu işaretle. Proje takvimdeki ilk boş günlere yerleşir.
 *
 * Kurulum: README_TR.md (aynı klasörde).  Anahtarlar sadece bu projenin "Script properties" alanında durur.
 */

const REPO = 'bugrahancamlibel/youtube-kanali';
const RAW = 'https://raw.githubusercontent.com/' + REPO;
const UP = 'https://api.upload-post.com';
const EL = 'https://api.elevenlabs.io';
const TZ = 'Europe/Istanbul';
const OFFSET = '+03:00';

const SH_PROJ = 'Projeler', SH_CAL = 'Takvim', SH_SET = 'Ayarlar', SH_LOG = 'Günlük';
const PROJ_HEAD = ['No', 'Proje', 'Uzun video başlığı', 'Durum', 'Onay', 'Ses', 'Videolar', 'Not', 'slug'];
const CAL_HEAD = ['Tarih', 'No', 'Proje', 'İçerik', 'Başlık', 'Platformlar', 'Durum', 'Sonuç', 'Deneme', 'İstek ID', 'Video', 'anahtar'];
const P = {no: 0, name: 1, title: 2, status: 3, ok: 4, voice: 5, link: 6, note: 7, slug: 8};
const K = {date: 0, no: 1, name: 2, kind: 3, title: 4, plats: 5, status: 6, result: 7, tries: 8, req: 9, video: 10, key: 11};
const KIND = {short1: 'Short 1', long: 'Uzun video', short2: 'Short 2'};
const OFFS = {short1: 0, long: 1, short2: 3};          // gün farkı: Short 1, ertesi gün uzun video, 2 gün sonra Short 2
const ST = {plan: 'planlandı', retry: 'tekrar denenecek', sent: 'gönderildi', live: 'yayında', partial: 'kısmen hata',
            fail: 'HATA', stop: 'durduruldu'};
const DEFAULTS = [
  ['upload_post_kullanici', '', 'Upload-Post profil (user) adı — ZORUNLU'],
  ['yayin_saati', '20:30', 'Yayın saati (Türkiye saati)'],
  ['short_platformlar', 'youtube,tiktok,instagram,facebook', 'Shorts nereye gitsin'],
  ['uzun_platformlar', 'youtube', 'Uzun video nereye gitsin'],
  ['ai_etiketi', 'evet', 'TikTok / Instagram / Facebook "AI ile üretildi" etiketi'],
  ['youtube_kategori', '28', '28 = Science & Technology'],
  ['facebook_page_id', '', 'Birden fazla Facebook sayfan varsa sayfa ID'],
  ['elevenlabs_voice_id', '', 'Boş bırakırsan "Max" sesi aranır'],
  ['eposta_bildirim', 'evet', 'Yayın / hata / onay e-postaları'],
  ['yayinlar_durduruldu', 'hayır', '"evet" yaparsan hiçbir şey gönderilmez'],
];

// ------------------------------------------------------------------ menü ve kurulum
function onOpen() {
  SpreadsheetApp.getUi().createMenu('YouTube')
    .addItem('Şimdi çalıştır', 'simdiCalistir')
    .addItem('Anahtarları gir', 'anahtarlariGir')
    .addSeparator()
    .addItem('Kurulum (ilk sefer)', 'kurulum')
    .addToUi();
}

function kurulum() {
  const ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(TZ);
  const proj = sheet_(SH_PROJ, PROJ_HEAD, [60, 170, 360, 110, 60, 220, 90, 260, 10]);
  const cal = sheet_(SH_CAL, CAL_HEAD, [150, 40, 150, 90, 330, 230, 120, 330, 60, 120, 70, 10]);
  sheet_(SH_LOG, ['Zaman', 'Olay'], [150, 900]);
  const set = sheet_(SH_SET, ['Ayar', 'Değer', 'Açıklama'], [190, 280, 380]);
  const have = set.getLastRow() > 1 ? set.getRange(2, 1, set.getLastRow() - 1, 1).getValues().map(r => r[0]) : [];
  DEFAULTS.forEach(d => { if (have.indexOf(d[0]) < 0) set.appendRow(d); });
  proj.hideColumns(P.slug + 1); cal.hideColumns(K.key + 1);
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'calis').forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('calis').timeBased().everyMinutes(15).create();
  PropertiesService.getScriptProperties().setProperty('SON_SENKRON', '0');
  calis();
  const miss = eksikler_();
  SpreadsheetApp.getUi().alert('Kurulum tamam. Sistem artık her 15 dakikada bir kendiliğinden çalışacak.' +
    (miss.length ? '\n\nEksikler:\n- ' + miss.join('\n- ') : '\n\nHer şey hazır.'));
}

function anahtarlariGir() {
  const ui = SpreadsheetApp.getUi(), pr = PropertiesService.getScriptProperties();
  [['UPLOAD_POST_API_KEY', 'Upload-Post API anahtarı'], ['ELEVENLABS_API_KEY', 'ElevenLabs API anahtarı'],
   ['GITHUB_TOKEN', 'GitHub token (youtube-kanali reposu, Contents: Read and write)']].forEach(k => {
    const r = ui.prompt(k[1], (pr.getProperty(k[0]) ? 'Kayıtlı. Değiştirmek için yenisini yapıştır, ' : '') +
      'boş bırakırsan değişmez.', ui.ButtonSet.OK_CANCEL);
    if (r.getSelectedButton() === ui.Button.OK && r.getResponseText().trim()) pr.setProperty(k[0], r.getResponseText().trim());
  });
  const miss = eksikler_();
  ui.alert(miss.length ? 'Kaydedildi. Eksikler:\n- ' + miss.join('\n- ') : 'Kaydedildi. Her şey hazır.');
}

function simdiCalistir() {
  PropertiesService.getScriptProperties().setProperty('SON_SENKRON', '0');
  calis();
  SpreadsheetApp.getActive().toast('Tamam. Ayrıntılar "Günlük" sayfasında.', 'YouTube', 5);
}

function eksikler_() {
  const pr = PropertiesService.getScriptProperties(), s = ayarlar_(), m = [];
  if (!pr.getProperty('UPLOAD_POST_API_KEY')) m.push('Upload-Post API anahtarı (menü: YouTube > Anahtarları gir)');
  if (!s.upload_post_kullanici) m.push('"Ayarlar" sayfasında upload_post_kullanici');
  if (!pr.getProperty('ELEVENLABS_API_KEY')) m.push('ElevenLabs API anahtarı (sadece seslendirme için)');
  if (!pr.getProperty('GITHUB_TOKEN')) m.push('GitHub token (sadece seslendirmeyi GitHub\'a koymak için)');
  return m;
}

// ------------------------------------------------------------------ ana döngü (her 15 dk)
function calis() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return;
  try {
    const pr = PropertiesService.getScriptProperties();
    const now = new Date();
    const hourly = now.getTime() - Number(pr.getProperty('SON_SENKRON') || 0) > 55 * 60 * 1000;
    if (hourly) {
      tryStep_('senkron', senkron_);
      pr.setProperty('SON_SENKRON', String(now.getTime()));
    }
    tryStep_('takvim', takvimeYerlestir_);
    tryStep_('kaydırma', kaydir_);
    tryStep_('yayın', yayinla_);
    if (hourly) {
      tryStep_('durum', durumKontrol_);
      tryStep_('ses', sesUret_);
    }
    tryStep_('sıralama', sirala_);
  } finally {
    lock.releaseLock();
  }
}

function tryStep_(name, fn) {
  try { fn(); } catch (e) { log_('HATA (' + name + '): ' + (e && e.stack || e)); }
}

// ------------------------------------------------------------------ GitHub'dan projeleri al
function senkron_() {
  const idx = getJson_(RAW + '/main/projects/index.json');
  if (!idx || !idx.projects) { log_('projects/index.json okunamadı'); return; }
  const sh = SpreadsheetApp.getActive().getSheetByName(SH_PROJ);
  const rows = data_(sh);
  idx.projects.forEach(slug => {
    const p = getJson_(RAW + '/main/projects/' + slug + '/project.json');
    if (!p) { log_('okunamadı: ' + slug); return; }
    const longU = (p.uploads || []).filter(u => u.id === 'long')[0] || {};
    const status = {ready: 'Hazır', needs_voice: 'Ses bekliyor', rejected: 'Reddedildi'}[p.status] || p.status;
    const i = rows.findIndex(r => r[P.slug] === slug);
    if (i < 0) {
      const link = 'https://github.com/' + REPO + '/tree/videolar/' + slug;
      sh.appendRow([p.number, p.name, longU.title || '', status, !!p.approved, '', link, p.note || '', slug]);
      const r = sh.getLastRow();
      sh.getRange(r, P.ok + 1).insertCheckboxes().setValue(!!p.approved);
      log_('yeni proje: ' + slug + ' (' + status + ')');
      if (p.status === 'ready' && !p.approved) bildir_('Onay bekliyor: ' + p.number + ' - ' + p.name, onayMetni_(p));
    } else {
      const r = i + 2, old = rows[i][P.status];
      if (old !== 'Reddedildi' && old !== status) {
        sh.getRange(r, P.status + 1).setValue(status);
        sh.getRange(r, P.title + 1).setValue(longU.title || '');
        log_(slug + ': ' + old + ' -> ' + status);
        if (p.status === 'ready' && !rows[i][P.ok]) bildir_('Onay bekliyor: ' + p.number + ' - ' + p.name, onayMetni_(p));
      }
    }
  });
}

function onayMetni_(p) {
  const base = 'https://github.com/' + REPO + '/blob/videolar/' + p.slug + '/';
  return p.number + ' - ' + p.name + ' hazır.\n\nİzle:\n- Short 1: ' + base + 'short1.mp4\n- Uzun video: ' + base +
    'long.mp4\n- Short 2: ' + base + 'short2.mp4\n\nBeğendiysen Google E-Tablosu\'nda "Projeler" sayfasında "Onay" kutusunu işaretle. ' +
    'Proje takvimdeki ilk boş günlere yerleşir.\n\nAyrıntılar: https://github.com/' + REPO + '/tree/main/projects/' + p.slug;
}

// ------------------------------------------------------------------ onaylı projeleri takvime koy
function takvimeYerlestir_() {
  const ss = SpreadsheetApp.getActive(), sh = ss.getSheetByName(SH_PROJ), cal = ss.getSheetByName(SH_CAL);
  const projs = data_(sh), rows = data_(cal), s = ayarlar_();
  projs.forEach(pr => {
    if (pr[P.ok] !== true || pr[P.status] !== 'Hazır') return;
    const slug = pr[P.slug];
    if (rows.some(r => String(r[K.key]).indexOf(slug + '/') === 0)) return;
    const p = getJson_(RAW + '/main/projects/' + slug + '/project.json');
    if (!p) return;
    const ups = (p.uploads || []).slice().sort((a, b) => (OFFS[a.id] || 0) - (OFFS[b.id] || 0));
    let dates;
    if (ups.every(u => u.publish_at)) {
      dates = ups.map(u => new Date(u.publish_at));
    } else {
      const all = data_(cal).map(r => r[K.date]).filter(d => d instanceof Date);
      let d0 = all.length ? addDays_(dayOf_(new Date(Math.max.apply(null, all))), 2) : null;
      const first = ilkBosGun_(s);
      if (!d0 || d0 < first) d0 = first;
      dates = ups.map(u => slot_(addDays_(d0, OFFS[u.id] || 0), s.yayin_saati));
    }
    ups.forEach((u, j) => {
      const plats = (u.type === 'short' ? s.short_platformlar : s.uzun_platformlar);
      cal.appendRow([dates[j], p.number, p.name, KIND[u.id] || u.id, u.title, plats, ST.plan, '', 0, '',
                     RAW + '/videolar/' + slug + '/' + u.asset, slug + '/' + u.id]);
    });
    log_('takvime alındı: ' + slug + ' -> ' + dates.map(d => fmt_(d)).join(', '));
    if (!ups.every(u => u.publish_at)) {
      bildir_('Takvime alındı: ' + p.number + ' - ' + p.name, ups.map((u, j) => '- ' + fmt_(dates[j]) + '  ' + (KIND[u.id] || u.id) +
        ': ' + u.title).join('\n'));
    }
  });
  formatCal_();
}

function ilkBosGun_(s) {           // bugünün yayın saatine en az 3 saat varsa bugün, yoksa yarın
  const today = dayOf_(new Date());
  const slotToday = slot_(today, s.yayin_saati);
  return slotToday.getTime() - Date.now() > 3 * 3600 * 1000 ? today : addDays_(today, 1);
}

// ------------------------------------------------------------------ plan gecikirse ileri kaydır
function kaydir_() {
  const ss = SpreadsheetApp.getActive(), cal = ss.getSheetByName(SH_CAL);
  const ok = onayliSluglar_(), rows = data_(cal);
  const open = rows.map((r, i) => [r, i]).filter(x => (x[0][K.status] === ST.plan || x[0][K.status] === ST.retry) &&
    x[0][K.date] instanceof Date && ok[slugOf_(x[0])]);
  if (!open.length) return;
  const earliest = Math.min.apply(null, open.map(x => x[0][K.date].getTime()));
  const late = Date.now() - earliest, grace = 6 * 3600 * 1000;
  if (late <= grace) return;
  let days = Math.ceil((late - grace) / 86400000);
  while (earliest + days * 86400000 < Date.now() - grace) days++;
  open.forEach(x => cal.getRange(x[1] + 2, K.date + 1).setValue(new Date(x[0][K.date].getTime() + days * 86400000)));
  log_('plan gecikmişti: kalan ' + open.length + ' yayın ' + days + ' gün ileri alındı (sıra ve aralıklar aynı)');
}

// ------------------------------------------------------------------ sırası geleni gönder
function yayinla_() {
  const s = ayarlar_(), pr = PropertiesService.getScriptProperties();
  const key = pr.getProperty('UPLOAD_POST_API_KEY');
  if (s.yayinlar_durduruldu === 'evet') return;
  const ss = SpreadsheetApp.getActive(), cal = ss.getSheetByName(SH_CAL);
  const ok = onayliSluglar_(), rows = data_(cal), now = Date.now();
  const due = rows.map((r, i) => [r, i]).filter(x => (x[0][K.status] === ST.plan || x[0][K.status] === ST.retry) &&
    x[0][K.date] instanceof Date && x[0][K.date].getTime() <= now + 5 * 60 * 1000 && ok[slugOf_(x[0])])
    .sort((a, b) => a[0][K.date] - b[0][K.date]).slice(0, 2);
  if (!due.length) return;
  if (!key || !s.upload_post_kullanici) {
    const pr2 = PropertiesService.getScriptProperties(), last = Number(pr2.getProperty('EKSIK_UYARI') || 0);
    if (Date.now() - last > 6 * 3600 * 1000) {
      log_('sırası gelen yayın var ama Upload-Post anahtarı / kullanıcı adı eksik (menü: YouTube > Anahtarları gir, Ayarlar sayfası)');
      pr2.setProperty('EKSIK_UYARI', String(Date.now()));
    }
    return;
  }
  const cache = {};
  due.forEach(x => {
    const r = x[0], row = x[1] + 2, slug = slugOf_(r), id = String(r[K.key]).split('/')[1];
    const p = cache[slug] || (cache[slug] = getJson_(RAW + '/main/projects/' + slug + '/project.json'));
    const u = p && (p.uploads || []).filter(v => v.id === id)[0];
    const tries = Number(r[K.tries] || 0) + 1;
    cal.getRange(row, K.tries + 1).setValue(tries);
    if (!u) { yaz_(cal, row, tries >= 3 ? ST.fail : ST.retry, 'project.json okunamadı'); return; }
    let plats = String(r[K.plats]).split(',').map(v => v.trim()).filter(Boolean);
    let res = gonder_(s, key, p, u, plats, r[K.video], tries, false);
    if (res.code === 403 && plats.indexOf('tiktok') >= 0) {
      plats = plats.filter(v => v !== 'tiktok');
      cal.getRange(row, K.plats + 1).setValue(plats.join(','));
      log_('TikTok bu Upload-Post planında yok; TikTok\'suz gönderiliyor');
      res = gonder_(s, key, p, u, plats, r[K.video], tries, false);
    }
    if (!res.ok && /url|download|fetch|indir/i.test(res.text)) {
      log_('video adresinden alınamadı, dosya olarak yükleniyor: ' + slug + '/' + id);
      res = gonder_(s, key, p, u, plats, r[K.video], tries, true);
    }
    if (res.ok) {
      cal.getRange(row, K.req + 1).setValue(res.body.request_id || res.body.job_id || '');
      yaz_(cal, row, ST.sent, 'gönderildi ' + fmt_(new Date()) + ' — platform sonuçları saat başı kontrol edilir');
      log_('gönderildi: ' + slug + '/' + id + ' -> ' + plats.join(','));
      bildir_('Yayına gönderildi: ' + u.title, (KIND[id] || id) + ' — ' + plats.join(', ') + '\n' + p.number + ' - ' + p.name);
    } else {
      const st = tries >= 3 ? ST.fail : ST.retry;
      yaz_(cal, row, st, 'HTTP ' + res.code + ': ' + res.text.slice(0, 400));
      log_('gönderilemedi (' + tries + '. deneme): ' + slug + '/' + id + ' HTTP ' + res.code + ' ' + res.text.slice(0, 300));
      if (st === ST.fail) bildir_('YAYIN HATASI: ' + u.title, '3 denemede gönderilemedi.\nSon hata: HTTP ' + res.code + ' ' +
        res.text.slice(0, 800) + '\n\nDüzeltince "Takvim" sayfasında Durum hücresini "tekrar denenecek", Deneme hücresini 0 yap.');
    }
  });
}

function gonder_(s, key, p, u, plats, videoUrl, tries, asFile) {
  const f = [['user', s.upload_post_kullanici]];
  plats.forEach(x => f.push(['platform[]', x]));
  f.push(['title', u.title], ['description', u.description || ''], ['async_upload', 'true'], ['external_id', p.slug + '/' + u.id]);
  const ai = s.ai_etiketi === 'hayır' ? 'false' : 'true';
  if (plats.indexOf('youtube') >= 0) {
    f.push(['categoryId', String(s.youtube_kategori || '28')], ['privacyStatus', 'public'], ['containsSyntheticMedia', 'false'],
           ['selfDeclaredMadeForKids', 'false']);
    (u.tags || []).forEach(t => f.push(['tags[]', t]));
  }
  if (plats.indexOf('tiktok') >= 0) f.push(['tiktok_title', u.caption || u.title], ['is_aigc', ai]);
  if (plats.indexOf('instagram') >= 0) f.push(['instagram_title', u.caption || u.title], ['is_ai_generated', ai]);
  if (plats.indexOf('facebook') >= 0) {
    f.push(['facebook_title', u.title], ['facebook_description', u.description || ''], ['facebook_is_ai_generated', ai]);
    if (s.facebook_page_id) f.push(['facebook_page_id', String(s.facebook_page_id)]);
  }
  let file = null;
  if (asFile) file = UrlFetchApp.fetch(videoUrl, {muteHttpExceptions: true}).getBlob().setName(u.asset).setContentType('video/mp4');
  else f.push(['video', videoUrl]);
  const mp = multipart_(f, file);
  const idem = (p.slug + '-' + u.id + '-a' + tries + '-' + plats.join('-') + (asFile ? '-f' : '')).replace(/[^A-Za-z0-9-]/g, '');
  const resp = UrlFetchApp.fetch(UP + '/api/upload', {method: 'post', contentType: mp.type, payload: mp.bytes,
    headers: {Authorization: 'Apikey ' + key, 'Idempotency-Key': idem}, muteHttpExceptions: true});
  const code = resp.getResponseCode(), text = resp.getContentText();
  let body = {};
  try { body = JSON.parse(text); } catch (e) {}
  return {ok: (code === 200 || code === 202) && body.success !== false, code: code, text: text, body: body};
}

function multipart_(fields, file) {
  const b = '----yt' + Utilities.getUuid().replace(/-/g, '');
  let bytes = [];
  const add = s => { bytes = bytes.concat(Utilities.newBlob(s).getBytes()); };
  fields.forEach(kv => add('--' + b + '\r\nContent-Disposition: form-data; name="' + kv[0] + '"\r\n\r\n' + kv[1] + '\r\n'));
  if (file) {
    add('--' + b + '\r\nContent-Disposition: form-data; name="video"; filename="' + file.getName() + '"\r\nContent-Type: video/mp4\r\n\r\n');
    bytes = bytes.concat(file.getBytes());
    add('\r\n');
  }
  add('--' + b + '--\r\n');
  return {type: 'multipart/form-data; boundary=' + b, bytes: bytes};
}

// ------------------------------------------------------------------ gönderilenlerin sonucu
function durumKontrol_() {
  const key = PropertiesService.getScriptProperties().getProperty('UPLOAD_POST_API_KEY');
  if (!key) return;
  const cal = SpreadsheetApp.getActive().getSheetByName(SH_CAL);
  data_(cal).forEach((r, i) => {
    if (r[K.status] !== ST.sent || !r[K.req]) return;
    const resp = UrlFetchApp.fetch(UP + '/api/uploadposts/status?request_id=' + encodeURIComponent(r[K.req]),
      {headers: {Authorization: 'Apikey ' + key}, muteHttpExceptions: true});
    if (resp.getResponseCode() !== 200) return;
    let b = {};
    try { b = JSON.parse(resp.getContentText()); } catch (e) { return; }
    const res = b.results || b.result;
    const st = String(b.status || '').toLowerCase();
    if (!res && ['completed', 'success', 'finished', 'done', 'failed', 'error'].indexOf(st) < 0) return;
    const parts = [], errs = [];
    const list = Array.isArray(res) ? res : Object.keys(res || {}).map(k => Object.assign({platform: k}, res[k]));
    list.forEach(x => {
      const name = x.platform || x.name || '?';
      if (x.success === false && !x.skipped) { errs.push(name); parts.push(name + ': HATA ' + (x.error || x.message || '')); }
      else if (x.skipped) parts.push(name + ': bağlı değil');
      else parts.push(name + ': ok' + (x.url ? ' ' + x.url : ''));
    });
    const final = errs.length ? ST.partial : (st === 'failed' || st === 'error' ? ST.fail : ST.live);
    yaz_(cal, i + 2, final, parts.join(' | ') || st);
    if (errs.length || final === ST.fail) bildir_('Yayın sorunu: ' + r[K.title], parts.join('\n') || st);
  });
}

// ------------------------------------------------------------------ seslendirme (ElevenLabs -> GitHub)
function sesUret_() {
  const pr = PropertiesService.getScriptProperties();
  const el = pr.getProperty('ELEVENLABS_API_KEY'), gh = pr.getProperty('GITHUB_TOKEN');
  const sh = SpreadsheetApp.getActive().getSheetByName(SH_PROJ);
  const rows = data_(sh);
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i], slug = r[P.slug], row = i + 2;
    if (r[P.status] !== 'Ses bekliyor' || /^hazır/.test(String(r[P.voice]))) continue;
    if (dosyaVar_(RAW + '/videolar/' + slug + '/vo.mp3')) { sh.getRange(row, P.voice + 1).setValue('hazır (GitHub\'da vo.mp3)'); continue; }
    if (!el || !gh) { sh.getRange(row, P.voice + 1).setValue('bekliyor: ElevenLabs anahtarı / GitHub token eksik'); continue; }
    const tr = UrlFetchApp.fetch(RAW + '/main/projects/' + slug + '/' + encodeURIComponent('ElevenLabs Metni.txt'), {muteHttpExceptions: true});
    if (tr.getResponseCode() !== 200) { sh.getRange(row, P.voice + 1).setValue('metin bulunamadı'); continue; }
    const text = tr.getContentText().trim();
    const H = {'xi-api-key': el};
    const sub = UrlFetchApp.fetch(EL + '/v1/user/subscription', {headers: H, muteHttpExceptions: true});
    if (sub.getResponseCode() === 200) {
      const s = JSON.parse(sub.getContentText()), left = (s.character_limit || 0) - (s.character_count || 0);
      if (left < text.length) {
        const msg = 'kredi yetersiz: kalan ' + left + ', gereken ' + text.length;
        if (r[P.voice] !== msg) {
          sh.getRange(row, P.voice + 1).setValue(msg);
          bildir_('Seslendirme bekliyor: ' + r[P.no] + ' - ' + r[P.name], 'ElevenLabs ' + msg + '. Kredi gelince kendiliğinden seslendirilecek.');
        }
        continue;
      }
    }
    const vid = sesId_(H);
    if (!vid) { sh.getRange(row, P.voice + 1).setValue('"Max" sesi bulunamadı: ElevenLabs\'te My Voices\'a ekle'); continue; }
    const audio = tts_(H, vid, text);
    if (!audio.ok) { sh.getRange(row, P.voice + 1).setValue('ses üretilemedi: ' + audio.err.slice(0, 200)); log_('TTS hata ' + slug + ': ' + audio.err); continue; }
    const put = UrlFetchApp.fetch('https://api.github.com/repos/' + REPO + '/contents/' + slug + '/vo.mp3', {
      method: 'put', contentType: 'application/json', muteHttpExceptions: true,
      headers: {Authorization: 'Bearer ' + gh, Accept: 'application/vnd.github+json'},
      payload: JSON.stringify({message: 'ses: ' + slug + ' (' + audio.model + ')', branch: 'videolar',
                               content: Utilities.base64Encode(audio.bytes)})});
    if (put.getResponseCode() === 201 || put.getResponseCode() === 200) {
      sh.getRange(row, P.voice + 1).setValue('hazır ' + fmt_(new Date()) + ' (' + audio.model + ')');
      log_('seslendirildi: ' + slug);
      bildir_('Seslendirildi: ' + r[P.no] + ' - ' + r[P.name], 'Ses GitHub\'a kondu. Pazartesi üretimi videoyu tamamlayıp onaya sunacak.');
    } else {
      sh.getRange(row, P.voice + 1).setValue('GitHub\'a yazılamadı: HTTP ' + put.getResponseCode());
      log_('GitHub PUT hata ' + slug + ': ' + put.getContentText().slice(0, 300));
    }
    return;                                   // her çalışmada en fazla bir seslendirme
  }
}

function sesId_(H) {
  const s = ayarlar_();
  if (s.elevenlabs_voice_id) return s.elevenlabs_voice_id;
  const r = UrlFetchApp.fetch(EL + '/v2/voices?search=Max&page_size=100', {headers: H, muteHttpExceptions: true});
  if (r.getResponseCode() !== 200) return '';
  const v = (JSON.parse(r.getContentText()).voices || []).filter(x => /^max/i.test(x.name || ''));
  v.sort((a, b) => (/documentary/i.test(b.name) - /documentary/i.test(a.name)));
  return v.length ? v[0].voice_id : '';
}

function tts_(H, vid, text) {
  const call = (t, model) => UrlFetchApp.fetch(EL + '/v1/text-to-speech/' + vid + '?output_format=mp3_44100_128', {
    method: 'post', contentType: 'application/json', headers: H, muteHttpExceptions: true,
    payload: JSON.stringify({text: t, model_id: model})});
  let err = '';
  for (const model of ['eleven_v4', 'eleven_v3']) {
    try {
      const r = call(text, model);
      if (r.getResponseCode() === 200) return {ok: true, bytes: r.getBlob().getBytes(), model: model};
      err = 'HTTP ' + r.getResponseCode() + ' ' + r.getContentText().slice(0, 300);
      if (r.getResponseCode() === 401 || /quota/i.test(err)) break;
    } catch (e) {                               // zaman aşımı: sahne sahne parçalayıp birleştir
      err = String(e);
      try {
        const parts = parcala_(text, 1200);
        let bytes = [];
        for (const p of parts) {
          const r = call(p, model);
          if (r.getResponseCode() !== 200) throw new Error('HTTP ' + r.getResponseCode() + ' ' + r.getContentText().slice(0, 200));
          bytes = bytes.concat(r.getBlob().getBytes());
        }
        return {ok: true, bytes: bytes, model: model + ' (' + parts.length + ' parça)'};
      } catch (e2) { err = String(e2); }
    }
  }
  return {ok: false, err: err};
}

function parcala_(text, max) {
  const lines = text.split(/\n\s*\n/), out = [];
  let cur = '';
  lines.forEach(l => {
    if (cur && (cur.length + l.length + 2) > max) { out.push(cur); cur = ''; }
    cur = cur ? cur + '\n\n' + l : l;
  });
  if (cur) out.push(cur);
  return out;
}

// ------------------------------------------------------------------ yardımcılar
function sheet_(name, head, widths) {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0) sh.appendRow(head);
  sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground('#1c2d72').setFontColor('#ffffff');
  sh.setFrozenRows(1);
  widths.forEach((w, i) => sh.setColumnWidth(i + 1, w));
  const def = ss.getSheetByName('Sheet1') || ss.getSheetByName('Sayfa1');
  if (def && def.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(def);
  return sh;
}

function data_(sh) {
  const n = sh.getLastRow() - 1;
  return n > 0 ? sh.getRange(2, 1, n, sh.getLastColumn()).getValues() : [];
}

function ayarlar_() {
  const sh = SpreadsheetApp.getActive().getSheetByName(SH_SET), o = {};
  DEFAULTS.forEach(d => { o[d[0]] = d[1]; });
  if (sh) data_(sh).forEach(r => { if (r[0]) o[String(r[0]).trim()] = String(r[1]).trim(); });
  if (!/^\d{1,2}:\d{2}$/.test(o.yayin_saati)) o.yayin_saati = '20:30';
  return o;
}

function onayliSluglar_() {
  const o = {};
  data_(SpreadsheetApp.getActive().getSheetByName(SH_PROJ)).forEach(r => { if (r[P.ok] === true && r[P.status] !== 'Reddedildi') o[r[P.slug]] = true; });
  return o;
}

function slugOf_(r) { return String(r[K.key]).split('/')[0]; }

function yaz_(cal, row, status, result) {
  cal.getRange(row, K.status + 1).setValue(status);
  cal.getRange(row, K.result + 1).setValue(result);
}

function sirala_() {
  const cal = SpreadsheetApp.getActive().getSheetByName(SH_CAL);
  if (cal.getLastRow() > 2) cal.getRange(2, 1, cal.getLastRow() - 1, CAL_HEAD.length).sort({column: 1, ascending: true});
  formatCal_();
}

function formatCal_() {
  const cal = SpreadsheetApp.getActive().getSheetByName(SH_CAL);
  if (cal.getLastRow() > 1) cal.getRange(2, 1, cal.getLastRow() - 1, 1).setNumberFormat('dd.mm.yyyy ddd hh:mm');
}

function getJson_(url) {
  const r = UrlFetchApp.fetch(url + (url.indexOf('?') < 0 ? '?' : '&') + 't=' + Date.now(), {muteHttpExceptions: true});
  if (r.getResponseCode() !== 200) return null;
  try { return JSON.parse(r.getContentText()); } catch (e) { return null; }
}

function dosyaVar_(url) {
  const r = UrlFetchApp.fetch(url, {headers: {Range: 'bytes=0-0'}, muteHttpExceptions: true});
  return r.getResponseCode() === 200 || r.getResponseCode() === 206;
}

function pad_(n) { return (n < 10 ? '0' : '') + n; }
function dayOf_(d) { return Utilities.formatDate(d, TZ, 'yyyy-MM-dd'); }            // 'YYYY-MM-DD' (Türkiye günü)
function addDays_(day, n) {
  const d = new Date(day + 'T12:00:00' + OFFSET);
  return dayOf_(new Date(d.getTime() + n * 86400000));
}
function slot_(day, hhmm) {
  const p = hhmm.split(':');
  return new Date(day + 'T' + pad_(Number(p[0])) + ':' + pad_(Number(p[1])) + ':00' + OFFSET);
}
function fmt_(d) { return Utilities.formatDate(d, TZ, 'dd.MM.yyyy HH:mm'); }

function log_(msg) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SH_LOG);
  if (!sh) return;
  sh.insertRowAfter(1);
  sh.getRange(2, 1, 1, 2).setValues([[fmt_(new Date()), String(msg).slice(0, 1500)]]);
  if (sh.getLastRow() > 600) sh.deleteRows(601, sh.getLastRow() - 600);
}

function bildir_(subject, body) {
  if (ayarlar_().eposta_bildirim === 'hayır') return;
  try {
    MailApp.sendEmail(Session.getEffectiveUser().getEmail(), '[YouTube] ' + subject,
      body + '\n\nPanel: ' + SpreadsheetApp.getActive().getUrl());
  } catch (e) { log_('e-posta gönderilemedi: ' + e); }
}
