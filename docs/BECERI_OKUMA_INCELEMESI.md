# Beceri okuma incelemesi — 2026-10-23

## BK: sayaç düzeltildi ve yayınlandı

Bütün standart beceri kitapları `50300` vnum'unu kullanır; beceri kimliği
`socket[0]` içindedir. `uibkoku.py` eski sayaçta yalnız vnum'a bakıyordu.
Seçilen Master becerinin soketiyle eşleşen kitap adetleri artık toplanıyor;
seçim/uygun kitap yoksa slot temizleniyor. İncelenen sunucu `BKBul` ve
`/bkoku` yolları vnum ile beceri soketini zaten birlikte kontrol ediyor.

Canlı sürüm: `1792749080`. Sekiz karışık envanter kontrolü, patchcheck 81/81,
JS ve CPython 3.13 sözdizimi kontrolleri geçti. Paketteki 2.224 dosyadan yalnız
`/uibkoku.py` değişti. Public adresten alınan modül adayla birebir eşleşti.
Gerçek oyun testi yapılmadı. Yedek: `/home/m2web/backups/bk-count-8ryxb3q5`.

## Ruh taşı: aynı sayaç hatası yok; ayrı doğrulama eksiği var

Standart ruh taşı `50513` beceriye özel değildir. Bütün uygun Grand Master
becerilerinde aynı eşya kullanıldığı için toplam adedinin gösterilmesi doğrudur.
Unutma kâğıdı `71001` ve Münzevi Tavsiyesi `71094` de ortak sarf malzemeleridir.

`apps/server/game/src/cmd_general.cpp` içindeki `do_ruhoku` ve `ruh_event`,
`LearnGrandMasterSkill(skillindex)` sonucundan bağımsız olarak ruh taşı tüketir.
Öğrenme fonksiyonu (`char_skill.cpp`, `LearnGrandMasterSkill`) geçersiz veya
uygun olmayan beceriyi reddetse de çağıran kod tüketimi sürdürür. İstemci
arayüzündeki seçim kontrolü, sunucunun kendi doğrulamasının yerini tutmaz.

Bu, normal okumada şansın tutmamasıyla aynı durum değildir: geçerli bir
okuma denemesinin başarısız olunca taş tüketmesi beklenir. İlerideki düzeltme
yalnız başarı dönüşünü kontrol ederek yapılmamalıdır; uygun beceri, öğrenilebilirlik
ve Grand Master kademesi sarf malzemeleri/derece harcanmadan önce doğrulanmalıdır.

Bu ek bulgu kaynak incelemesine dayanır; canlıda geçersiz komut gönderilerek
denenmedi. BK sayacı yayınına sunucu değişikliği eklenmedi.
