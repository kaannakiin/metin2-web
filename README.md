# Anka2 Game Server & Client Projesi

## 📋 Proje Hakkında

Bu proje, Anka2 MMORPG oyunu için geliştirilmiş sunucu ve istemci kaynak kodlarını içermektedir. Proje, modern C++ standartları kullanılarak geliştirilmiş ve optimize edilmiştir.

### ⚠️ Önemli Notlar

- **FoxFS Formatı**: FoxFS'nin düzgün çalışması için `.rar` dosyasındaki formatı takip edin. Dosya yapısını ve dizin organizasyonunu değiştirmeyin.
- **Kod Temizliği**: Proje kodları %75 oranında temizlenmiştir. Ölü kodlar ve yorum satırları tamamen kaldırılmıştır.
- **Client Temizliği**: Client tarafında tekrarlanan eşyalar, moblar, yorum satırları ve kullanılmayan kodlar temizlenmiştir.
- **Lokalizasyon**: Mob sohbetleri, OX Quiz ve locale_string artık client'tan `locale/[lang]` dizininden yüklenmektedir. Görev çevirileri hala `[lang]/translate.lua` dosyasından yüklenmektedir. Yakında görev çevirileri de client tarafına taşınacaktır.

---

## 🏗️ Altyapı Bilgileri

- **Altyapı**: Mainline
- **İşletim Sistemi**: FreeBSD 13.3 ve üzeri
- **Veritabanı**: MariaDB 10.6 (MySQL uyumlu client / libmysqlclient)
- **Server Derleyici**: ccache clang++-devel (C++2a/C++20 standardı)
- **Client Derleyici**: Visual Studio 2022 (v143 toolset)
- **Server C++ Standardı**: C++2a (C++20)
- **Client C++ Standardı**: C++17 (Debug), C++20 (Release)
- **Server Mimari**: 32-bit (x32)
- **Client Mimari**: 32-bit (Win32)
- **Build Sistemi**: Makefile (Server), Visual Studio Solution (Client)
- **Önbellek**: ccache (Server derleme hızlandırma)

---

## 📁 Proje Yapısı

### Client (Binary)

```
apps/client/
├── source/                    # Kaynak kodlar
│   ├── UserInterface/        # Ana kullanıcı arayüzü modülü (182 dosya)
│   ├── GameLib/              # Oyun mantığı kütüphanesi (98 dosya)
│   ├── EterLib/              # Eter altyapı kütüphanesi (157 dosya)
│   ├── EterBase/             # Temel yardımcı sınıflar
│   ├── EterGrnLib/           # Granny model sistemi
│   ├── EterImageLib/         # Görüntü işleme kütüphanesi
│   ├── EterLocale/           # Lokalizasyon desteği
│   ├── EterPack/             # Paket dosyası yönetimi
│   ├── EterPythonLib/        # Python 2.7 entegrasyonu
│   ├── EffectLib/            # Parçacık efektleri
│   ├── ScriptLib/            # Script yönetimi
│   ├── SpeedTreeLib/         # SpeedTree entegrasyonu
│   ├── SphereLib/            # Fizik motoru
│   ├── MilesLib/             # Ses sistemi
│   ├── Discord/              # Discord RPC entegrasyonu
│   └── CWebBrowser/          # Web tarayıcı entegrasyonu
├── extern/                    # Harici kütüphaneler
│   ├── include/              # Header dosyaları
│   │   ├── boost/            # Boost C++ kütüphaneleri
│   │   ├── cryptopp/         # Crypto++ şifreleme
│   │   ├── Python-2.7/       # Python 2.7 headers
│   │   ├── d3d9/             # DirectX 9 headers
│   │   ├── FoxFS.h           # FoxFS dosya sistemi
│   │   └── ...
│   └── library/              # Derlenmiş kütüphaneler (.lib)
├── vs_files/                 # Visual Studio proje dosyaları
└── client.sln                # Visual Studio solution dosyası
```

**Client Modülleri:**
- **UserInterface**: Ana oyun arayüzü, ağ yönetimi, oyuncu yönetimi, envanter sistemi
- **GameLib**: Oyun nesneleri, aktörler, çarpışma tespiti, hareket sistemi
- **EterLib**: Grafik motoru, DirectX 9 wrapper, render sistemi
- **EterPythonLib**: Python script entegrasyonu, UI modülleri
- **EffectLib**: Parçacık efektleri, ışık efektleri, görsel efektler

### Server

```
apps/server/
├── game/                     # Oyun sunucusu
│   └── src/                  # Kaynak kodlar (316 dosya)
│       ├── char.cpp          # Karakter yönetimi
│       ├── item.cpp          # Eşya sistemi
│       ├── questmanager.cpp  # Görev yönetimi
│       ├── mob_manager.cpp   # Mob yönetimi
│       ├── guild.cpp         # Lonca sistemi
│       ├── party.cpp         # Parti sistemi
│       ├── shop.cpp          # Dükkan sistemi
│       ├── dungeon.cpp       # Zindan sistemi
│       └── ...
├── db/                       # Veritabanı sunucusu
│   └── src/                  # Kaynak kodlar
│       ├── DBManager.cpp     # Veritabanı yönetimi
│       ├── ClientManager.cpp # İstemci yönetimi
│       └── ...
├── common/                   # Ortak header dosyaları
│   ├── service.h             # Servis tanımlamaları
│   ├── singleton.h           # Singleton pattern
│   └── ...
└── library/                  # Sunucu kütüphaneleri
    ├── libthecore/           # Çekirdek kütüphane
    ├── liblua/               # Lua script motoru
    ├── libsql/               # SQL wrapper
    ├── libgame/              # Oyun yardımcıları
    └── ...
```

**Server Modülleri:**
- **game/src**: Ana oyun sunucusu, karakter yönetimi, savaş sistemi, görev sistemi
- **db/src**: Veritabanı sunucusu, SQL sorguları, veri yönetimi
- **library**: Paylaşılan kütüphaneler (Lua, SQL, çekirdek)

---

## 🔧 Derleme Gereksinimleri

### Server (FreeBSD)

**Gerekli Paketler:**
```bash
pkg install boost-all cryptopp ccache llvm-devel gmake devil lzo2 \
             mariadb106-server mariadb106-client python27 openssl \
             makedepend subversion binutils
```

**Build Komutları:**
```bash
cd apps/server/game/src
make clean
make
```

**Özellikler:**
- FreeBSD 13.3+ gereklidir
- ccache clang++-devel derleyici kullanılır
- C++20 (C++2a) standardı
- 32-bit (x32) mimari
- Makefile tabanlı build sistemi
- ccache ile hızlandırılmış derleme
- MariaDB 10.6 client (libmysqlclient uyumlu)

### Client (Windows)

**Gereksinimler:**
- Visual Studio 2022 (v143 toolset)
- Windows SDK 10.0
- Python 2.7 (development headers)

**Build Komutları:**
```batch
cd Source\Binary
# Visual Studio'da client.sln dosyasını açın
# Release x32 konfigürasyonunu seçin
# Build > Rebuild Solution
```

**Özellikler:**
- Visual Studio 2022 solution
- C++17 (Debug) / C++20 (Release)
- Precompiled headers kullanımı
- Multi-processor compilation
- 16 adet statik kütüphane projesi

---

## 🛠️ Kullanılan Teknolojiler

### Client Tarafı

- **Programlama Dili**: C++17/C++20
- **Grafik API**: DirectX 8
- **Script Dili**: Python 2.7
- **Kütüphaneler**:
  - Boost C++ Libraries
  - Crypto++ (şifreleme)
  - FoxFS (dosya sistemi)
  - Granny2 (3D model formatı)
  - DevIL (görüntü işleme)
  - LZ4/LZO (sıkıştırma)
  - RapidJSON (JSON işleme)
  - Discord RPC (Discord entegrasyonu)

### Server Tarafı

- **Programlama Dili**: C++20 (C++2a)
- **Script Dili**: Lua 5.x
- **Veritabanı**: MariaDB 10.6
- **Kütüphaneler**:
  - Boost C++ Libraries
  - Crypto++ (şifreleme)
  - Lua (script motoru)
  - Custom SQL wrapper
  - Custom core library (libthecore)

---

## ✨ Özellikler

Proje, `common/service.h` dosyasında tanımlanan 300+ özellik flag'i ile genişletilebilir bir yapıya sahiptir:

- 🐾 Pet Sistemi
- 🐴 Binek Sistemi
- 📜 Görev Sistemi (Lua tabanlı)
- 🏰 Lonca Sistemi (Guild System)
- 👥 Parti Sistemi
- 🛒 Çevrimdışı Pazar
- 👗 Kostüm Sistemi
- 🌍 Çoklu Dil Desteği
- 💎 Premium Sistemi (Kaldırıldı)
- 🏛️ Zindan Sistemi
- 🎣 Avcılık Sistemi
- 🐉 Resmi Pet Sistemi
- 🔬 Biyolog Sistemi (yeni altyapı)
- 🎫 Savaş Bileti / Battle Pass (Normal + Premium)
- 🌐 Global sıralama
- ✨ Ruh kalıntısı (kalıntı bonusu)
- 📛 Ünvan (başlık) sistemi
- 🏆 Şampiyon seviye sistemi
- Ve daha fazlası...

---

## 🔒 Güvenlik ve Performans

### Güvenlik Önlemleri

Proje, aşağıdaki güvenlik önlemlerini içermektedir:

1. **SQL Injection Koruması**
   - Tüm kullanıcı girdileri `DBManager::EscapeString()` ile sanitize edilir
   - Parametreli sorgular kullanılır

2. **Buffer Overflow Koruması**
   - `strlcpy`, `snprintf` gibi güvenli fonksiyonlar kullanılır
   - Buffer boyut kontrolleri yapılır

3. **Null Pointer Kontrolleri**
   - SQL sorgu sonuçları kontrol edilir
   - Pointer kullanımlarından önce null kontrolü yapılır

4. **Integer Overflow Kontrolleri**
   - GOLD_MAX gibi maksimum değer kontrolleri
   - Aritmetik işlemlerde overflow kontrolü

5. **Memory Leak Önleme**
   - `std::unique_ptr` kullanımı
   - RAII prensiplerine uyum

### Performans Optimizasyonları

- SQL sorguları optimize edilmiştir
- Gereksiz sorgu tekrarları önlenmiştir
- Buffer yönetimi optimize edilmiştir

---

## 📜 Lisans ve Kullanım

Bu proje eğitim ve araştırma amaçlıdır. Ticari kullanım için gerekli lisansları kontrol edin.

---

## 👥 Katkıda Bulunanlar

- **Altyapı**: Mainline
- **Kod Temizleme**: %75 ölü kod temizliği yapılmıştır
- **Güvenlik Düzeltmeleri**: SQL injection, buffer overflow, null pointer kontrolleri eklendi
- **Performans Optimizasyonları**: SQL sorgu optimizasyonları ve memory leak önlemleri

---

## 💬 Destek

Sorularınız için proje issue'larını kullanabilirsiniz.

---

**Not**: Bu dokümantasyon proje yapısına göre oluşturulmuştur. Gerçek kod yapısı ve özellikler kaynak kodları inceleyerek doğrulanmalıdır.

---

## 📅 Son Güncellemeler (2026)

- **Altyapı**: FreeBSD sürümü yükseltildi; veritabanı **MariaDB 10.6**; FreeBSD tarafında kurulumu kolaylaştıran özel script (talimatlar konsolda; ayrıntı `CHANGELOG_2026.md`).
- **Oyun**: Yeni biyolog; çevrimdışı pazar / depo / sistem seçenekleri / otomatik av düzeltmeleri; zindan ve dünya patronu notice; vuruş-kaçırma; client kamera; binek/kaykay rotasyon; şaman skill ve animasyon düzeltmeleri; skill 6–9 etkin.
- **Araçlar**: DumpProto Release `.txt` kapatma davranışı iyileştirildi.
- **Client**: İsteğe bağlı `ENABLE_BINARY_SERVERINFO` — sunucu bilgisi `PythonNetworkStreamModule.cpp` / binary üzerinden.

**Tam liste:** `CHANGELOG_2026.md`

---

## İletişim

- 💻 **GitHub:** [github.com/ybeststudio](https://github.com/ybeststudio)
- 🎧 **Discord Server:** [discord.gg/NXmc6JrwYr](https://discord.gg/NXmc6JrwYr)
- 🆔 **Discord ID:** beststudio
- 🌐 **Web:** [beststudio.dev](https://beststudio.dev)
- 💬 **TurkMMO Forum:** [Best Studio](https://forum.turkmmo.com/uye/2104546-best-studio/)
- 📺 **YouTube:** [@ybeststudio](https://www.youtube.com/@ybeststudiostr)
- 📷 **Instagram:** [@ybeststudio](https://www.instagram.com/ybeststudio)
- 👥 **Facebook:** [ybeststudio](https://www.facebook.com/ybeststudio/)
- 🐦 **Twitter:** [@ybeststudio](https://twitter.com/ybeststudio)
- 🎵 **TikTok:** [@ybeststudio](https://tiktok.com/@ybeststudio)
