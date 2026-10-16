# Değişiklik Notları - 2026

## Yapılan Düzeltme ve Değişiklikler (Güncel Özet)

Aşağıdaki madde listesi, depodaki güncel sürümle uyumlu özet değişiklik kaydıdır. Ayrıntılı teknik notlar için ilgili kaynak dosyalara ve commit geçmişine bakın.

### Altyapı ve ortam

1. **FreeBSD** sürümü yükseltildi.
2. **MariaDB 10.6** sürümüne yükseltildi.
3. **FreeBSD** tarafında kurulum/işletmeyi kolaylaştıran özel script eklendi; talimatlar FreeBSD ana ekranda gösterilir.

### Sistemler ve arayüz

4. **Yeni Biyolog sistemi** eklendi (eski sistem kaldırıldı).
5. **Sistem seçenekleri** sorunu düzeltildi.
6. **Çevrimdışı pazar** kurma sorunu düzeltildi.
7. **Depo** açılmama sorunu düzeltildi.
8. **Otomatik av** hataları düzeltildi.

### Client ve oynanış

9. **Client kamera** hatası düzeltildi.
10. **İtem çakışması** ve **zindan bileti** ile ilgili sorunlar düzeltildi.
11. **Akzadur zindanı** düzeltildi.
12. **Dünya patronu** (2504 M591) **notice** sorunları düzeltildi.
13. **Vuruş / kaçırma** sorunu düzeltildi.
14. Bazı **zindanlarda core** hatası ve **Şeytan Kulesi** demirci **+ basma** sorunu düzeltildi.
15. Tüm **binekler** ve **kaykaylarda **sağ/sol rotasyon\*\* ayarlandı.
16. **Şaman**, sörf tahtası üzerindeki **çift yelpaze** animasyonu düzeltildi.
17. **6, 7, 8, 9** yeni **skill**’ler etkinleştirildi; resmi davranışa uygun çalışır.
18. **Şaman** becerileri düzeltildi: **Kükreme**, **Ejderha Atışı**.

### Yeni özellikler

19. **Savaş bileti (Battle Pass)**: **Normal** ve **Premium** olmak üzere iki çizgi eklendi.
20. **Global sıralama** eklendi.
21. **Ruh kalıntısı** sistemi (**kalıntı bonusu**).
22. **Ünvan sistemi** (başlık).
23. **Şampiyon seviye** sistemi.

### Araçlar ve düzeltme

24. **DumpProto** Release modunda **.txt** dosyalarını kapatmama sorunu giderildi; davranış iyileştirildi.
25. **Sunucu bilgisini binary üzerinden aktarma**: `ENABLE_BINARY_SERVERINFO` — tüm portlar ve sunucu adı client binary üzerinden okunur; ilgili dosya: `Source/Binary/source/UserInterface/PythonNetworkStreamModule.cpp`.

---

## Özet tablo

| #     | Konu                                                     | Tür                |
| ----- | -------------------------------------------------------- | ------------------ |
| 1–3   | FreeBSD, MariaDB 10.6, yardımcı script                   | Altyapı            |
| 4–8   | Biyolog, seçenekler, çevrimdışı pazar, depo, otomatik av | Sistem             |
| 9–18  | Client, zindan, patron, savaş, binek, şaman, skill       | Düzeltme / oynanış |
| 19–23 | Battle Pass, sıralama, kalıntı, ünvan, şampiyon seviye   | Özellik            |
| 24–25 | DumpProto, binary sunucu bilgisi                         | Araç / client      |

---

## Notlar

- Paket yapısı veya `#pragma pack` ile ilgili değişiklikler yapıldıysa, client–sunucu sürümlerinin uyumlu olduğundan emin olun.
- `ENABLE_BINARY_SERVERINFO` kullanımı için `common/service.h` (veya projedeki tanım) ile client tarafının aynı anda derlendiğini doğrulayın.

---

## Önceki detaylı kayıt (arşiv)

Aşağıdaki başlıklar, bu dosyanın önceki sürümünde tek tek dosya/satır referanslarıyla tutuluyordu; güncel tek kaynak olarak yukarıdaki özet liste kullanılmaktadır.

- NPC/binek/pet skill damage ve boss saldırı düzeltmesi (`char_skill.cpp` – `ComputeSkill`)
- Zindan kat atlatma nesneleri + basma / takas (`input_main.cpp`)
- Dil değiştirme `HORSE_LEVEL4` (`localeinfo.py`)
- Item / Battle Pass tooltip temizleme (`uicommon.py`, `uibattlepass.py`)
- Zehir hasarı null pointer core (`char_battle.cpp` – `Damage`)
- Otomatik toplama beceri kitabı birleşmesi (`char_item.cpp`, `char_battle.cpp`)

Bu maddelerin güncel kodda durumu için ilgili dosyalarda arama yapmanız önerilir.
