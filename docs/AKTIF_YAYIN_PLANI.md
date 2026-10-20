# Aktif yayın planı — 20 Ekim 2026

Kullanıcı bütün işleri sırayla uygulayıp iş bitiminde canlıya almamızı istedi.
Oyun testi kullanıcıda; gerekli derleme ve dosya/servis kontrolleri yapılır.

- [x] Silahçı, zırhçı ve market önerilerini gerçek mağaza stoklarına uygula.
- [x] Silahçıya 30 seviye silah ailelerini +9 koy; aynı ailelerin tüm
      geliştirme seviyelerini metin droplarından çıkar. Bosslar ayrı kapsamdır.
- [x] Sınıf seçimi sonrası yalnız standart/at becerilerini maksimum aç;
      ana becerilerin BK → G → P ilerlemesini koru. Yeni ve mevcut karakterler.
- [x] Yeni başlayanlara kalıcı savaşabilen zırhlı/askeri at ve çağırma aracı ver;
      yedi günlük süreli binek bitince karakter atsız kalmasın.
- [x] Yang miktarını orta-kolay hedefe göre artır; gerçek önce/sonra değerleri kaydet.
- [x] Efsunlanabilen her eşya grubunu ve mevcut havuzlarını tabloya çıkar;
      klasik düzenden sapmaları ayrı göster. Rastgele toplu bonus silme yok.
- [x] Sunucu/istemci APPLY kimliği uyuşmazlığını düzelt; Dolunay'daki
      PvM ortalamasının “Metinlere karşı güçlü” görünmesinin kaynağı budur.
- [x] Kaynak, SQL, görev nesneleri ve istemci paketini hazırla; önceki sürümü
      yedekleyerek toplu canlı kurulum yap. Main commit/push, yayın kaydı.

Kesin kullanıcı kararı: ana beceriler doğrudan P yapılmaz. Silahçıdaki 30
silahların ortalama/beceri zararı oyunun mevcut üretim kuralından gelir;
özel yüksek ortalama veya elle beş savaş bonusu basılmaz.

Canlı: ana paket `20261020-172132`, dolu envanterde destek becerisi düzeltmesi
`20261020-172626`. Efsun ve NPC tabloları ilgili rehberlerde. Oyun testi yapılmadı.
