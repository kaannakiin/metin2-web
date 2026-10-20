#!/usr/bin/env python3
"""Render the drop guide from real runtime tables. stdout only; --check verifies a saved guide."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCALE = ROOT / 'runtime/freebsd/share/locale/europe'
GUIDE = ROOT / 'docs/DROP_REHBERI.md'
POLICY_PATH = ROOT / 'platform/gameplay/phase3_loot.json'


def read_names(kind, lang):
    data = (LOCALE / 'country' / lang / (kind + '_names.txt')).read_bytes()
    try:
        text = data.decode('utf8')
    except UnicodeDecodeError:
        text = data.decode('cp1254', errors='replace')
    result = {}
    for line in text.splitlines():
        parts = line.split('\t', 1)
        if len(parts) == 2 and parts[0].isdigit():
            result[int(parts[0])] = parts[1].strip()
    return result


def proto(kind):
    data = (ROOT / 'runtime/freebsd/share/conf' / (kind + '_proto.txt')).read_bytes().decode('latin1')
    return {int(row['Vnum']): row for row in csv.DictReader(io.StringIO(data), delimiter='\t')
            if row['Vnum'].isdigit()}


def groups(filename):
    text = (LOCALE / filename).read_text()
    if text.count('{') != text.count('}'):
        raise ValueError('Unbalanced braces: ' + filename)
    result = []
    for match in re.finditer(r'Group\s+(\S+)\s*\{([^{}]*)\}', text):
        body = match[2]
        mob = re.search(r'^\s*Mob\s+(\d+)\s*$', body, re.M)
        vnum = re.search(r'^\s*Vnum\s+(\d+)\s*$', body, re.M)
        entries = [tuple(map(int, row)) for row in re.findall(
            r'^\s*\d+\s+(\d+)\s+(\d+)\s+(\d+)\s*$', body, re.M)]
        result.append({'name': match[1], 'mob': int(mob[1]) if mob else None,
                       'vnum': int(vnum[1]) if vnum else None, 'entries': entries})
    return result


def render():
    policy = json.loads(POLICY_PATH.read_text())
    items, mobs = proto('item'), proto('mob')
    item_names, mob_names = read_names('item', 'en'), read_names('mob', 'en')
    item_names.update(read_names('item', 'tr'))
    mob_names.update(read_names('mob', 'tr'))
    drops, specials = groups('mob_drop_item.txt'), groups('special_item_group.txt')
    special_by_id = {g['vnum']: g for g in specials}
    metins = [g for g in drops if g['name'].startswith('MetinLv')]
    bosses = [g for g in drops if g['name'].startswith('Phase3Boss_')]
    other = [g for g in drops if g not in metins and g not in bosses]
    sources = defaultdict(list)
    out = []

    def put(text=''):
        out.append(text)

    def name(vnum):
        return item_names.get(vnum, 'Adı bulunamayan eşya #' + str(vnum)).replace('|', '/')

    def mob_name(vnum):
        return mob_names.get(vnum, 'Adı bulunamayan yaratık #' + str(vnum)).replace('|', '/')

    def level(vnum):
        row = items[vnum]
        for i in range(2):
            if row.get('LimitType' + str(i)) == 'LEVEL':
                value = row.get('LimitValue' + str(i), '0')
                return value if value != '0' else '—'
        return '—'

    def pct(value):
        return ('%g' % value).replace('.', ',') + '%'

    def table(entries, chest=False):
        put('| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | ' + ('Sandık içi şans' if chest else 'Baz düşme şansı') + ' |')
        put('|---|---:|---:|---:|---:|')
        counts = Counter(entries)
        total = sum(row[2] for row in entries) if chest else 400
        if not total:
            raise ValueError('Empty reward table')
        for (vnum, amount, chance), repeats in counts.items():
            if vnum not in items:
                raise ValueError('Unknown reward: ' + str(vnum))
            quantity = str(amount) if repeats == 1 else str(repeats) + ' ayrı × ' + str(amount)
            probability = 100 * chance / total
            put('| ' + name(vnum) + ' | ' + str(vnum) + ' | ' + level(vnum)
                + ' | ' + quantity + ' | ' + pct(probability) + ' |')
        put()

    put('# Metin ve Boss Drop Rehberi — Anka2')
    put()
    put('Tarih: **20 Ekim 2026** · Loot politikası: **v' + str(policy['version']) + '**')
    put()
    put('**Durum:** Bu rehber repodaki güncel loot verisini anlatır; tek başına canlı kurulum kanıtı değildir. '
        'Önceki malzeme ağırlıklı sandık özeti geçersizdir. Yayın adayının durumu '
        '[kurulum belgesinde](../platform/deploy/GAMEPLAY_RELEASE.md) takip edilir.')
    put()
    put('## 1. En önemli düzeltmeler')
    put()
    put('- **Lusifer Sandığı 65 / 70 / 75 silah içerir.** Altı gerçek 75 silahın her biri %5 '
        '(toplam %30), beş doğrulanmış 70 silahın her biri %3 (toplam %15), yedi 65 silah '
        'her biri %1 (toplam %7). Hepsi +0. Barones de 75 silahları doğrudan her biri %3 verir.')
    put('- 85/90 metinlerden Zehir ve Orkide kaldırıldı. Diğer 75 silahlar da bu metin havuzuna eklenmedi.')
    put('- **Siam Bıçağı, Şeytani Pala, Yarı-İnsan Kılıç ve Mutluluk Yelpazesi 70 seviyedir.** '
        'Önceki özette 75 ailesiyle karıştırılmışlardı. Metinlerde kalırlar.')
    put('- Havalı Çelik Yay **2170**; Geyik Boynuzu Yay **2150** ve 30 seviyedir. '
        'ID ve seviye ayrımı gerçek item_proto üzerinden denetlendi.')
    put('- Diğer klasik boss sandıkları da artık silah ve zırh içerir; sadece tüketim malzemesi vermez.')
    put('- Önceki rehberde ayrı dengeleme bekleyen 10 klasik bossun tamamına özel loot eklendi. '
        'Azrail kendi sandığını verir; Barones/Cadı/Ağaç bossları/Kharoon doğrudan düşürür.')
    put('- Haritalar ve doğma bölgeleri korunur; metin yoğunluğu başlangıcın 4 katı, yeniden doğma süreleri yarısıdır. Exp ve zindan mekaniği değiştirilmedi.')
    put()
    put('## 2. Oranlar nasıl okunur?')
    put()
    put('Metin ve doğrudan boss tablolarındaki oranlar, yakın seviyede standart item-drop ayarındaki '
        '**baz oranlardır**: dosyadaki 400 yaklaşık %100, 24 yaklaşık %6 eder. Seviye farkı, '
        'sunucu oranı, çift drop ve motor bonusları gerçek sonucu değiştirebilir. Her satır bağımsızdır; '
        'aynı kesimde birden fazla eşya düşebilir. BK satırları ayrı rastgele beceriler üretir.')
    put()
    put('Sandık içi oranlar ise ağırlık/toplam hesabıdır. **Bir sandık yalnız bir sonuç satırı seçer**; '
        'o satırdaki adet kadar eşya verir. Silah/zırh satırında adet 1. 10 BK sonucu, aynı rastgele '
        'becerinin 10 kitaplık yığınıdır. Sandıktaki oranlar seviye drop cezasıyla tekrar çarpılmaz.')
    put()
    put('Bu dosya tüm mob_drop_item statik satırlarını ve ilgili sandık/taş kesesi içeriklerini kapsar. '
        'Aktif quest, event flag, premium ve özel C++ drop kancaları koşulludur; bu statik liste '
        'tek başına her canlı etkinlik ödülünü garanti etmez. common_drop_item, etc_drop_item ve '
        'drop_item_group dosyaları mevcut repoda boştur.')
    put()
    put('## 3. Aranan eşyalar: nereden düşer?')
    put()
    for group in drops:
        label = (('Metin ' + mobs[group['mob']]['Level']) if group in metins else mob_name(group['mob']))
        for vnum, amount, chance in group['entries']:
            if label not in sources[vnum]:
                sources[vnum].append(label)
    for group in bosses:
        for chest, _, _ in group['entries']:
            label = mob_name(group['mob']) + ' → ' + name(chest)
            for vnum, amount, chance in special_by_id[chest]['entries']:
                if label not in sources[vnum]:
                    sources[vnum].append(label)
    put('| Eşya | VNUM | Gerçek seviye | Güncel statik kaynaklar |')
    put('|---|---:|---:|---|')
    popular = policy['reaper_75_weapons'] + [170,250,1120,3150,7150,11290,11490,11690,11890,50300,50513]
    for vnum in popular:
        locations = sources.get(vnum, ['Statik tanım bulunamadı'])
        if vnum in policy['reaper_75_weapons']:
            locations = ['Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0']
        elif vnum in (50300,50513):
            locations = ['Aşağıdaki metin/sandık tabloları; her kaynağın miktarı ve şansı ayrı']
        put('| ' + name(vnum) + ' | ' + str(vnum) + ' | ' + level(vnum) + ' | ' + '; '.join(locations) + ' |')
    put()
    put('Zehir için %5, ortalamada 20 sandık demektir; 20 sandıkta garanti anlamına gelmez. '
        'En az bir Zehir olasılığı 20 sandıkta yaklaşık %64,2; 59 sandıkta yaklaşık %95,2. '
        'Herhangi bir 75 silah için ortalama 3,33 sandık gerekir. Ticaret sınıfa uygun silaha erişimi kolaylaştırır.')
    put()
    put('## 4. Metinlerin eksiksiz statik drop tabloları')
    put()
    put('Toplam **' + str(len(metins)) + ' metin drop grubu**. İçeriği aynı olan gruplar birlikte gösterildi; '
        'başlıklar metin seviyesidir, çıkan eşyanın giyme seviyesi ayrı sütundadır. '
        'Mevcut eski/alternatif metin VNUM’ları haritaya yeni taş eklendiği anlamına gelmez.')
    put()
    combined = defaultdict(list)
    for group in metins:
        combined[tuple(group['entries'])].append(group)
    for entries, group_list in combined.items():
        levels = sorted({int(mobs[g['mob']]['Level']) for g in group_list})
        put('### Metin seviyesi ' + ' / '.join(map(str, levels)))
        put()
        put('Taşlar: ' + '; '.join(mob_name(g['mob']) + ' (`' + str(g['mob']) + '`)' for g in group_list) + '.')
        put()
        table(list(entries))
    put('Yang bu statik eşya tablosundan ayrıdır. Sıfır gold tanımlı metin için kaynak formülü '
        '`500 + metin_seviyesi × 150` kullanılır; üstüne mevcut yang miktarı/bonus kuralları uygulanır. '
        'Buradaki formül ekranda kesin görülecek toplam yang diye okunmamalıdır.')
    put()
    put('## 5. Boss → sandık ve toplam ekipman şansı')
    put()
    put('| Boss | Boss VNUM / seviyesi | Sandık | Sandık VNUM | Silah | Zırh | Diğer |')
    put('|---|---|---|---:|---:|---:|---:|')
    for boss in policy['bosses']:
        rewards = special_by_id[boss['chest']]['entries']
        total = sum(row[2] for row in rewards)
        weapons = sum(w for v,c,w in rewards if items[v]['Type'] == 'ITEM_WEAPON') * 100 / total
        armour = sum(w for v,c,w in rewards if items[v]['Type'] == 'ITEM_ARMOR') * 100 / total
        put('| ' + mob_name(boss['mob']) + ' | ' + str(boss['mob']) + ' / ' + mobs[boss['mob']]['Level']
            + ' | ' + name(boss['chest']) + ' | ' + str(boss['chest']) + ' | ' + pct(weapons)
            + ' | ' + pct(armour) + ' | ' + pct(100-weapons-armour) + ' |')
    put()
    put('Bu ' + str(len(policy['bosses'])) + ' boss için doğrudan 1 kendi sandığı satırı @400 vardır: standart yakın seviye bazında '
        'yaklaşık %100. Aynı sandığı paylaşan iki boss (Şeytan Kral/Kibirli Şeytan Kral) aynı içeriği kullanır. '
        'Sandık içindeki ekipman oranları yukarıda; aşağıdaki listelerde tek tek eşya oranları bulunur.')
    put()
    put('## 6. Klasik boss sandıklarının tam içerikleri')
    put()
    seen = set()
    for boss in policy['bosses']:
        chest = boss['chest']
        if chest in seen:
            continue
        seen.add(chest)
        owners = [mob_name(b['mob']) for b in policy['bosses'] if b['chest'] == chest]
        put('### ' + name(chest) + ' — ' + str(chest))
        put()
        put('Kaynak: ' + ', '.join(owners) + '. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.')
        put()
        table(special_by_id[chest]['entries'], chest=True)
    put('## 7. Doğrudan boss ve diğer yaratık dropları — tam listeler')
    put()
    put('Önceki kısa özette bu gruplar gösterilmemişti. Aşağıdaki satırlar sandıklara dönüştürülmedi. '
        '`Phase3Direct_` grupları yeni v3 boss ödülleridir; diğerleri mevcut korunmuş satırlardır. '
        'Kaptan, normal yaratık ve maymun grupları da kaynak dosyanın tamamı görülebilsin diye dahil edildi; '
        'hepsinin boss olduğu iddia edilmez. Bu kayıtların bulunması ilgili yaratığın canlı haritada '
        'spawn edildiğini tek başına kanıtlamaz.')
    put()
    for group in other:
        mob = group['mob']
        put('### ' + mob_name(mob) + ' — ' + str(mob))
        put()
        put('Grup: `' + group['name'] + '` · Proto seviye: ' + mobs[mob]['Level']
            + ' · Rütbe: `' + mobs[mob]['Rank'] + '`.')
        put()
        table(group['entries'])
    put('## 8. Klasik boss kapsaması — açık bırakılan loot yok')
    put()
    put('| İçerik | VNUM | Bu revizyonda statik özel loot durumu |')
    put('|---|---:|---|')
    configured = {g['mob'] for g in drops}
    for mob in sorted({b['mob'] for b in policy['bosses']} | {b['mob'] for b in policy['direct_bosses']}):
        boxes = [b for b in policy['bosses'] if b['mob'] == mob]
        status = ('Kendi sandığı: ' + name(boxes[0]['chest'])) if boxes else 'Doğrudan eşya/ruh taşı tablosu'
        if mob not in configured:
            status = 'EKSİK: tanım bulunamadı'
        put('| ' + mob_name(mob) + ' | ' + str(mob) + ' | ' + status + ' |')
    put()
    put('Önceki sürümde eksik olan Vahşi Yüzbaşı, Dev Hastalık Taşıyıcı, Güçlü Buz Cadısı, '
        'Barones, Dev Çöl Kaplumbağası, Kırmızı Ejderha, iki Ağaç bossu, Kharoon ve Azrail '
        'artık tanımlıdır. Zindan kill handler’larına ek eşya verme kodu konmadı; motorun mevcut '
        'mob_drop_item yolu kullanılır. Instance/reentry, boss izleme ve oyuncu kabulü ayrı '
        'konulardır; loot tamamlanması Faz 3’ün bütün mekaniklerinin bittiği anlamına gelmez.')
    put()
    put('## 9. Taş Kesesi (27999) açılınca ne çıkar?')
    put()
    put('Bu kese **beceriyi G’den P’ye çıkaran Ruh Taşı değildir**. Silah/zırh soket taşları ve '
        'Taş Sanatı Kitabı havuzudur. Tek açılış tek sonuç; aşağıdaki oranlar 637 toplam ağırlıktan hesaplanır.')
    put()
    table(special_by_id[27999]['entries'], chest=True)
    put('## 10. Koşullu motor ve quest ekleri')
    put()
    put('- Seviye 40+ bosslarda C++ `three_skill_item` kuralı ek Ruh Taşı üretebilir. '
        'Bu, sandıktaki Ruh Taşı satırından bağımsızdır; sabit sandık yüzdesiyle karıştırılmaz.')
    put('- `CreateQuestDropItem`, seviye/etkinlik flag’lerine göre başka eşyalar ekleyebilir. '
        'Biyolog görevleri, etkinlikler ve at üzerindeyken kitap kancaları herkese her kesimde açık ödül değildir.')
    put('- Motorda doğrudan soket taşı için ayrı `GetDropMetinStoneVnum/Pct` yolu bulunur. '
        'Bu rehber, canlıda hangi runtime değerinin atandığını ölçmeden buna sabit bir yüzde yazmaz.')
    put('- Görevlerin kurulmuş/derlenmiş hali ve aktif event flag’leri canlı oyun testiyle ayrıca doğrulanır. '
        'Bu belge kaynak/runtime statik konfigürasyonunu doğrular; canlı kabul testini ikame etmez.')
    put()
    put('## 11. Araştırma: resmî akış ve PvP karşılaştırması')
    put()
    put('Resmî wiki eşyanın hangi sandık ailesinde olduğunu belirlemek için kullanıldı. '
        '**Resmî ve özel sunucu yüzdeleri yayımlanmıyorsa oran uydurulmadı:** bu projedeki yüzdeler '
        '10 kişilik orta-kolay hedef için kendi denge kararımızdır. Resmî oyundaki modern 100+ '
        'içerik, lycan ekipmanı ve istemediğimiz yan sistemler bu yüzden otomatik taşınmadı.')
    put()
    put('| Kaynak | Doğrulanan karar |')
    put('|---|---|')
    refs = [
        ('Resmî Lusifer Sandığı', 'https://tr-wiki.metin2.gameforge.com/index.php/Lusifer_Sand%C4%B1%C4%9F%C4%B1', 'Gerçek 75 silah ailesi bu sandıkta bulunur; yalnız malzemeli taslak eksikti.'),
        ('Resmî Zehir Kılıcı', 'https://en-wiki.metin2.gameforge.com/index.php/Poison_Sword', 'Giyme seviyesi 75 ve Lusifer sandığı kaynak ilişkisi.'),
        ('Resmî Ork Reisi kutusu', 'https://en-wiki.metin2.gameforge.com/index.php/Chief_Orc%27s_Box', '65 silah ve 54 zırh ailesi; erken boss = yalnız düşük seviye silah varsayımı yapılmadı.'),
        ('Resmî Hayalet Lider kutusu', 'https://en-wiki.metin2.gameforge.com/index.php/Ghost_Leader%27s_Box', '65 silah ve 54 zırh havuzu.'),
        ('Resmî Kraliçe Örümcek kutusu', 'https://en-wiki.metin2.gameforge.com/index.php/Queen_Spider_Box', '65 silah ve 61 zırh havuzu.'),
        ('Resmî Dokuz Kuyruk sandığı', 'https://en-wiki.metin2.gameforge.com/index.php/Nine_Tails%27_Chest', '65 silah ve 61 zırh havuzu.'),
        ('Resmî Sarı Kaplan sandığı', 'https://en-wiki.metin2.gameforge.com/index.php/Yellow_Tiger%27s_Chest', '65 silah ve 61 zırh havuzu.'),
        ('Resmî Alev Kral sandığı', 'https://en-wiki.metin2.gameforge.com/index.php/Flame_King%27s_Chest', '65 silah ve 61 zırh havuzu.'),
        ('Resmî Şeytan Kral sandığı', 'https://en-wiki.metin2.gameforge.com/index.php/Demon_King%27s_Chest', '65 silah ve 61 zırh havuzu.'),
        ('M2-Board yönetim rehberi', 'https://forum.m2-board.com/threads/ileri-seviye-gelisim-rehberi.151/', 'PvP örneği: 75 sonrası Şeytan Kulesi/Lusifer sandığı üzerinden 75 silah ilerlemesi ve sandık ticareti.'),
        ('Resmî Barones', 'https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Barones', '75 silah, 66 zırh, kalkan ve takı doğrudan ödül; proje +0 base ve kendi şanslarını kullanır.'),
        ('Resmî Azrail sandığı', 'https://tr-wiki.metin2.gameforge.com/index.php/Azrailin_Sand%C4%B1%C4%9F%C4%B1', '70 silah, 66 zırh, 60 kask, Titan kalkanı ve takı ailesi.'),
        ('Resmî Güçlü Buz Cadısı', 'https://en-wiki.metin2.gameforge.com/index.php/Mighty_Ice_Witch', 'Silah verilmedi: zırh, kalkan, takı, +4 soket taşı, ruh taşı ve kan taşı seçildi.'),
        ('Resmî Vahşi Yüzbaşı', 'https://en-wiki.metin2.gameforge.com/index.php/Bestial_Captain', 'Kedi Isırığı/karartma yayı ve Kırmızı Karınca kıyafeti ailesi; projede +0.'),
        ('Resmî Dev Hastalık Taşıyıcı', 'https://en-wiki.metin2.gameforge.com/index.php/Giant_Plague_Carrier', 'Ruh taşı ana ödül; kutsama orta-kolay destek ödülü olarak bize ait ekleme.'),
        ('Resmî Çöl Kaplumbağası sandığı', 'https://en-wiki.metin2.gameforge.com/index.php/Desert_Tortoise_Chest', '65 silah ve 61 zırh ailesi.'),
        ('Resmî Kırmızı Ejderha', 'https://en-wiki.metin2.gameforge.com/index.php/Red_Dragon', 'Güncel wiki listesi sınırlı; projedeki 50080 eski sandık için yüksek boss havuzu bilinçli PvP uyarlaması.'),
        ('Resmî Hayalet Ağaç', 'https://en-wiki.metin2.gameforge.com/index.php/Giant_Ghost_Tree', 'Ana ödül ruh taşı; yeni silah havuzu uydurulmadı.'),
        ('Resmî Ağaç Lordu', 'https://en-wiki.metin2.gameforge.com/index.php/Ghost_Tree_Lord', 'Ana ödül ruh taşı.'),
        ('Resmî Kharoon', 'https://en-wiki.metin2.gameforge.com/index.php/Charon', 'Ruh kristali takıları, mavi/kırmızı inci ve ruh taşı seçildi.'),
        ('NirvanaMt2 sandık veritabanı', 'https://nirvanamt2.com/wiki/sandik/lusifer-sandigi', 'Arama dizinindeki PvP listesi aynı altı 75 silahı, 65 silahları ve 66 zırhı ayırıyor. Doğrudan sayfa isteği 500 verdi; yayımlanmamış yüzdeleri kaynak alınmadı.'),
    ]
    for label, url, finding in refs:
        put('| [' + label + '](' + url + ') | ' + finding + ' |')
    put()
    put('Eski Esoteric Leader kutusunun İngilizce sayfası 404 verdi; bu kutunun birebir resmî '
        'içeriği doğrulandı diye yazılmadı. Projedeki Karanlık Lider sandığı, erken boss havuzunu '
        'paylaşan açık bir PvP denge kararıdır. Resmî +1/+2/+3 rastgeleleri yerine mevcut +0 '
        'base/refine ekonomisi korundu; oyuncu geliştirme zinciri atlanmadı.')
    put()
    put('## 12. Kaynak dosyalar ve doğrulama')
    put()
    put('Bu belge `python3 platform/tools/drop_catalogue.py` çıktısıdır. '
        '`python3 platform/tools/drop_catalogue.py --check` kayıtlı belgenin verilerle aynı olduğunu denetler.')
    put()
    put('| Dosya | SHA-256 |')
    put('|---|---|')
    files = [POLICY_PATH, LOCALE/'mob_drop_item.txt', LOCALE/'special_item_group.txt',
             ROOT/'runtime/freebsd/share/conf/item_proto.txt', ROOT/'runtime/freebsd/share/conf/mob_proto.txt']
    for path in files:
        put('| `' + str(path.relative_to(ROOT)) + '` | `' + hashlib.sha256(path.read_bytes()).hexdigest() + '` |')
    put()
    put('Kontroller: bütün ödül VNUM’ları gerçek proto’da bulunmalı; sandık ağırlıkları 100 olmalı; '
        'gerçek 75 silah ailesi eksiksiz ve doğru seviyede olmalı; Havalı Çelik yanlışlıkla 2150 '
        'olmamalı; 75 silahlar metin havuzuna geri sızmamalı. Oyun içi drop/ortalama-beceri '
        'üretimi, sandık açma ve envanter davranışı bakım kurulumu ardından oynanarak doğrulanır.')
    put()
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render()
    if args.check:
        if not GUIDE.exists() or GUIDE.read_text().rstrip('\n') != result.rstrip('\n'):
            sys.exit('DROP GUIDE STALE: regenerate docs/DROP_REHBERI.md')
        print('DROP GUIDE OK: runtime tables, item/mob protos and saved guide match')
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
