# YouTube Yayın Paneli — kurulum (~10 dk, bir kere)

Yayın motoru Google'ın sunucularında çalışır (ücretsiz). Bilgisayarın kapalı olabilir; GitHub Actions gerekmez.

## 1. Tabloyu ve kodu oluştur
1. [sheets.new](https://sheets.new) ile yeni boş bir Google E-Tablosu aç, adını **YouTube Yayın Paneli** yap.
2. Menüden **Uzantılar → Apps Script**.
3. Açılan editörde `Kod.gs` içindeki her şeyi sil; bu klasördeki [`Kod.gs`](Kod.gs) dosyasının tamamını yapıştır
   (GitHub'da dosyayı açıp sağ üstteki "Copy raw file" düğmesiyle kopyalayabilirsin). **Kaydet** (disket ikonu).
4. Üstteki fonksiyon listesinden **kurulum**'u seç → **Çalıştır**.
5. Google izin isteyecek: hesabını seç → "Google bu uygulamayı doğrulamadı" uyarısında **Gelişmiş → (güvenli değil) sayfasına git**
   → **İzin ver**. (Kod senin hesabında, sadece senin tablon ve e-postan için çalışıyor.)
6. Tabloya dön: "Projeler", "Takvim", "Ayarlar", "Günlük" sayfaları oluşmuş, ilk 3 proje takvimde olacak.

## 2. Anahtarlar (sadece bu Google projesinde saklanır)
Tabloyu yenile (F5) → üstte **YouTube** menüsü çıkar → **Anahtarları gir**:
- **Upload-Post API anahtarı:** upload-post.com → hesap aç → bir profil (user) oluştur → YouTube, TikTok, Instagram,
  Facebook hesaplarını bağla → API Keys → yeni anahtar.
- **ElevenLabs API anahtarı:** elevenlabs.io → Developers → API Keys. ("Max - Elearning and Documentary" sesi
  hesabında "My Voices"ta olmalı.)
- **GitHub token:** github.com/settings/personal-access-tokens/new → Fine-grained → Repository access: *Only select
  repositories* → `youtube-kanali` → Permissions: **Contents: Read and write** → Generate. (Sadece seslendirmeyi
  GitHub'a koymak için.)

Sonra **Ayarlar** sayfasında `upload_post_kullanici` satırına Upload-Post profil adını yaz.

## 3. Kontrol
**YouTube → Şimdi çalıştır**, sonra **Günlük** sayfasına bak. Hata yoksa bitti; sistem her 15 dakikada bir kendi çalışır.

## Nasıl kullanılır
- **Takvim** sayfası: ne zaman ne yayınlanacak, durumu ne. Tarihi elle değiştirebilirsin.
- **Onay:** yeni video hazır olunca e-posta gelir; **Projeler** sayfasında o projenin **Onay** kutusunu işaretle.
  Takvimdeki ilk boş günlere otomatik yerleşir (Short 1 → ertesi gün uzun video → 2 gün sonra Short 2, saat 20:30).
- **Durdurmak:** Projeler'de Onay kutusunu kaldır (o proje durur) ya da Ayarlar'da `yayinlar_durduruldu` = `evet` (hepsi durur).
- Bir gün kaçarsa plan, sıra ve aralıklar korunarak ileri kayar; videolar üst üste yığılmaz.
- Upload-Post planın TikTok'a izin vermiyorsa o gönderi TikTok'suz yapılır.
- Videolar GitHub reposundan herkese açık adresle alınır, bu yüzden repo **public** kalmalı.
