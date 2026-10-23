# YouTube Kanalı: bulutta üretim ve yayın

Bilgisayarın kapalıyken de çalışır. Üç parça var:

| Parça | Ne yapar | Nerede |
|---|---|---|
| **Üretim** | Her pazartesi 09:32 Claude gündemden konu seçer, animasyonu ve 2 Shorts'u yapar | Claude zamanlanmış görevi (bulut) |
| **Depo** | Kod, proje bilgileri, videolar | Bu repo (`main` = kod/projeler, `videolar` dalı = mp4'ler) |
| **Yayın paneli** | Seslendirme (ElevenLabs), onay, takvim, Upload-Post ile yayın | Google E-Tablosu + Apps Script (ücretsiz) |

Kurulum: [`google-apps-script/KURULUM.md`](google-apps-script/KURULUM.md)

## Akış
1. Claude yeni projeyi hazırlar, metni `projects/<NN-isim>/ElevenLabs Metni.txt` olarak koyar.
2. Google paneli kredi varsa sesi üretir ve `videolar/<NN-isim>/vo.mp3` olarak GitHub'a koyar.
3. Claude sesi animasyona oturtur, final uzun video + 2 Shorts'u `videolar` dalına yükler, projeyi "hazır" yapar.
4. Panel sana **"Onay bekliyor"** e-postası atar; E-Tablo'da **Onay** kutusunu işaretlersin.
5. Panel takvime yerleştirir ve her gün 20:30'da sırası geleni YouTube / TikTok / Instagram / Facebook'a gönderir.

İlk 3 video (AI Jobs, Solar Superstorm, Deepfakes) onaylı olarak takvimde. 04 (Quantum Q-Day) ve 05 (Doomsday Glacier) ses bekliyor.

## Klasörler
- `projects/index.json` — panelin okuduğu proje listesi
- `projects/<NN-isim>/project.json` — başlıklar, açıklamalar, etiketler, durum (`ready` / `needs_voice`)
- `factory/` — üretim kodu ve haftalık talimatlar (`factory/README.md`)
- `google-apps-script/Kod.gs` — yayın paneli kodu
