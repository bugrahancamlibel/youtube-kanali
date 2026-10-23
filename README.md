# YouTube Kanalı: bulutta üretim ve yayın

Bilgisayarın kapalıyken de çalışır. Her şey GitHub'da durur:

| Ne | Nerede |
|---|---|
| Videolar | **Releases** (her proje için `long.mp4`, `short1.mp4`, `short2.mp4`) |
| Proje bilgileri ve yayın durumu | `projects/<NN-isim>/project.json`, `Bilgiler.txt` |
| Yayın takvimi | [`YAYIN_TAKVIMI.md`](YAYIN_TAKVIMI.md) (otomatik güncellenir) |
| Üretim kodu | `factory/` (haftalık Claude çalışması bunu kullanır) |
| Otomasyon | `.github/workflows/` (GitHub Actions) |

## Nasıl çalışır
1. **Üretim (her pazartesi, Claude, bulutta):** gündemden konu seçer, senaryoyu yazar, animasyonu yapar,
   sesi ElevenLabs API'den alır, uzun video + 2 Shorts üretir. Videoları Release'e yükler ve
   **`[Onay] ...` başlıklı bir issue açar** (GitHub'dan bildirim gelir, videoları Claude uygulamasında da izleyebilirsin).
2. **Onay (sen):** o issue'ya **`onay`** yazarsın (beğenmediysen **`ret`**). Telefondan GitHub uygulamasıyla da olur.
   Onaylanan proje takvimdeki ilk boş günlere otomatik yerleşir.
3. **Yayın (GitHub Actions, her gün 20:35 ve 21:35):** sırası gelen videoyu Upload-Post üzerinden
   YouTube / TikTok / Instagram / Facebook'a gönderir. Sıra: Short 1 → ertesi gün uzun video → 2 gün sonra Short 2;
   sonraki proje 2 gün sonra başlar. Saat 20:30. Bir gün kaçarsa plan, sıra ve aralıklar korunarak ileri kayar.

İlk 3 video (AI Jobs, Solar Superstorm, Deepfakes) onaylı olarak takvimde.

## Tek seferlik kurulum (sen yapmalısın, ~15 dk)
1. **Upload-Post:** upload-post.com'da hesap aç, bir profil (user) oluştur, YouTube, TikTok, Instagram (Business/Creator)
   ve Facebook Sayfası hesaplarını bu profile bağla. API Keys bölümünden bir anahtar oluştur.
   (Ücretsiz plan: ayda 10 yükleme ve TikTok yok. Haftada 1 konu için Basic plan gerekir.
   TikTok izin verilmezse sistem otomatik olarak TikTok'suz gönderir.)
2. **Anahtarı GitHub'a koy:** bu repoda *Settings → Secrets and variables → Actions → New repository secret*
   - Name: `UPLOAD_POST_API_KEY`, Secret: Upload-Post anahtarın
3. **Profil adını yaz:** `config.json` içinde `"upload_post_user": "KULLANICI_ADINI_YAZ"` kısmına Upload-Post profil adını yaz
   (GitHub'da dosyayı açıp kalem ikonuyla düzenle → Commit). Facebook'ta birden fazla sayfan varsa `facebook_page_id` de doldur.
4. **ElevenLabs (seslendirme için):** ElevenLabs → Developers → API Keys'ten bir anahtar oluştur, aynı yerden
   `ELEVENLABS_API_KEY` adıyla secret olarak ekle. "Max - Elearning and Documentary" sesi hesabındaki "My Voices"ta olmalı.
5. **Test:** *Actions → Yayin → Run workflow*, "Sadece planı göster" işaretli. Çıktıda hata olmamalı.

Anahtarları kimseyle (Claude dahil) paylaşma; sadece GitHub Secrets'a gir.

## Sık işler
- **Takvime bakmak:** `YAYIN_TAKVIMI.md`
- **Bir yayını durdurmak:** ilgili `project.json` içinde `"approved": false` yap.
- **Her şeyi durdurmak:** *Actions → Yayin → ⋯ → Disable workflow*
- **Hata olursa:** sistem `yayin-hatasi` etiketli bir issue açar, içinde ne olduğu yazar.
- **Saat / platform değiştirmek:** `config.json` (`publish_time`, `short_platforms`, `long_platforms`). Saati değiştirirsen
  `.github/workflows/yayin.yml` içindeki cron saatini de 5 dk sonrasına ayarla (cron UTC'dir, Türkiye = UTC+3).
