# Aktif NPC kurulumu

`ENABLE_RENEWAL_SHOPEX` açıktır. Silahçı (9001/9007), zırhçı (9002/9008)
ve market (9003) yalnız `player.shopex` / `player.shopex_item` üzerinden yüklenir.
Kanonik stok: `platform/tools/npc_profile.py stock()`. Dosya mağazası, eski
shop +9/trim SQL dosyaları ve tek seferlik NPC yayın betikleri kaldırıldı.
Diğer NPC'lerin standart shop kayıtları korunur.

Stok değişikliğinde önce `PVP_HEDEF.md`, sonra `stock()` güncellenir.
`npc_profile.py sql` tam profil migration'ını, `repair_sql` yalnız aktif
mağazaların onarımını, `report` oyuncu stok rehberini üretir. Bunların çıktıları
sırasıyla `20261020_npc_support.sql`, `20261021_npc_profile.sql` ve
`docs/NPC_CANLI_STOK.md` ile eşleşmelidir. Fresh seed aynı profilin üretilmiş
kopyasını içerir; eski stoklar yeniden eklenmez.

Güncel stok yayını: `platform/deploy/progression_release.py --npc-stock --install`.
Yalnız aktif SQL stoklarını günceller; görevler, binary ve istemci korunur.
DB yedeği ve hazırlık/kurulum arası değişiklik kontrolü vardır. Tüm yeni satırlar
fiyat/adet/efsun/soketleriyle eşleşmeden servisler başlatılmaz.

İlk onarımın tarihî yayın yolu: `platform/deploy/progression_release.py --npc-profile` hazırlığı;
`--install` ayrıca yedekli kurulum yapar. Bu sürümün baseline'ı `faaf95e85`tir;
yeni sürümde canlı kaynaklarla baseline güncellenmeden eski paket tekrar
uygulanmaz. Dosyalar/binary/DB değişmişse kurulum durur. Derleme ayrı kopyada
yapılır; live game dosyası servisler durduktan sonra değiştirilir.

Kurulum sonrası salt okunur kontrol:
`python3 platform/tools/npc_profile_verify.py`. Sekme ve ürün sayısından fazla
olarak NPC eşleşmesi, fiyat, adet, para türü, soket ve yedi efsun alanının tamamı
karşılaştırılır. Aynı NPC'nin standart shop kaydı varsa kontrol başarısızdır.
Bu kontrol oyun içinde pencere açma/satın alma testi yerine geçmez.

Destek ve kalıcı atın güncel akışı `starter_support.lua` içindedir. Login,
levelup ve tek döngü zamanlayıcısı kullanılır; standart/at becerileri 5. seviyede
tamamlanır. Ana beceriler BK/G/P kalır. Oyun kabulünü kullanıcı yapar.
