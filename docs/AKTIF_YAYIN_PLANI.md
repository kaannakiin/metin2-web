# Aktif yayın planı — 21 Ekim 2026

21 Ekim onarımı: önceki dosya yayını aktif DB mağazalarını doldurmamıştı.
Güncel mağazalar `shopex` / `shopex_item`; eski dosya ve stok girişleri kaldırıldı.
Destek becerileri 5. seviyede, login/levelup ve gerçek döngü zamanlayıcısıyla verilir.

Kullanıcı bütün işleri sırayla uygulayıp iş bitiminde canlıya almamızı istedi.
Oyun testi kullanıcıda; gerekli derleme ve dosya/servis kontrolleri yapılır.

- [x] Silahçı, zırhçı ve market önerilerini gerçek mağaza stoklarına uygula.
- [x] Silahçıya 30 seviye silah ailelerini +9 koy; aynı ailelerin tüm
      geliştirme seviyelerini metin droplarından çıkar. Bosslar ayrı kapsamdır.
- [x] 5. seviyede yalnız standart/at becerilerini maksimum aç;
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

Canlı onarım: `20261021-072726`; aktif SQL mağazaları, 5. seviye destek
becerileri ve kalıcı at. Önceki paketler tarihîdir. Efsun ve NPC tabloları
ilgili rehberlerde. Oyun testi kullanıcıda.
