# Rapor Yol Haritasi

Bu belge, proje icin IEEE-benzeri final raporun nasil yazilacagini, hangi sirayla ilerlenmesi gerektigini ve hangi malzemelerin rapora donusturulecegini netlestirir.

## Hedef Format

Onerilen format:

- `IEEE conference` stiline benzeyen `iki sutunlu` yapi
- `Overleaf + IEEE Conference Template` kullanimi
- Atif stili: `numarali IEEE referans stili` (`[1]`, `[2]`, ...)
- `Kapak + Icindekiler + teknik govde` iceren hibrit ders raporu yapisi

Pratik tercih:

- En guvenli secenek `Overleaf` uzerindeki `Official IEEE Conference Template`
- Eger LaTeX kullanmak istemezsek Word ile benzer gorunum taklit edilebilir, ancak atif ve bicim tutarliligi acisindan `LaTeX` daha temizdir

Not:

- Klasik IEEE konferans makalelerinde genelde `Icindekiler` bolumu bulunmaz
- Ancak bu proje bir `ders raporu` oldugu icin `IEEE-benzeri gorunum` korunup on tarafa `Icindekiler` eklenmesi daha dogru olur
- Yani hedefimiz `birebir IEEE submission` degil, `IEEE duzenine benzeyen duzgun teknik rapor`

## Hedef Uzunluk

Bu proje icin iyi bir hedef:

- `6-8 sayfa` ana rapor
- gerekiyorsa ek olarak `ekler` bolumu

Bu uzunluk, odevi anlatmak icin yeterli ama gereksiz yere sisik olmayan bir rapor cikarir.

## Raporun Ana Hikayesi

Rapor boyunca anlatacagimiz ana hikaye su olacak:

`Sentetik otobus telemetrisi MQTT ile buluta aktarilmis, AWS uzerinde gercek zamanli olarak islenmis, DynamoDB'de saklanmis ve FastAPI ile Streamlit dashboard uzerinden canli olarak izlenmistir.`

Bu hikaye bozulmamali. Rapor, sadece ekran goruntusu gosteren bir dokuman degil; `veri akisi + bulut isleme + depolama + gorsellestirme` zincirini savunan teknik bir metin olmali.

## Onerilen Bolumler

### 0. Kapak

Kapakta su bilgiler olmali:

- universite / ders bilgisi
- proje basligi
- ogrenci adi
- ogrenci numarasi
- teslim tarihi
- ders / ogretim elemani

### 1. Icindekiler

Bu bolum zorunlu olacak.

Icerik:

- ana bolumler
- varsa alt bolumler
- sayfa numaralari

Istersek ek olarak:

- `Sekiller Listesi`
- `Tablolar Listesi`

ama bunlar mecburi degil.

### 2. Baslik

Onerilen baslik:

`EGO-Benzeri Sentetik Veri ile Gercek Zamanli Otobus Takip ve Yogunluk Analiz Sistemi`

### 3. Ozet

Bu bolum kisa ve yogun olmali:

- problem nedir
- ne gelistirildi
- hangi teknolojiler kullanildi
- ne sonuc elde edildi

Uzunluk:

- `150-250 kelime`

### 4. Anahtar Kelimeler

Onerilen anahtar kelimeler:

- `MQTT`
- `AWS IoT Core`
- `Kinesis Data Streams`
- `AWS Lambda`
- `DynamoDB`
- `FastAPI`
- `Streamlit`
- `real-time bus tracking`

### 5. Giris

Burada sunlari anlatacagiz:

- toplu tasimada gercek zamanli takip neden onemli
- canli konum, ETA ve yogunluk bilgisinin neden degerli oldugu
- bu projede neden sentetik veri kullanildigi
- calismanin katkisi

Bu bolumde literatur veya genel teknik baglam verilir. Ama en fazla `1-1.5 sayfa` olmali.

### 6. Problem Tanimi ve Kapsam

Burada net cizgi cekilecek:

- gercek EGO verisi kullanilmadi
- sistem `EGO-benzeri` olarak modellendi
- telemetri ve kart basim verisi sentetik uretildi
- `ETA`, `estimated alighting`, `occupancy`, `delay` bulutta hesaplandi

Bu bolumde ayrica proje sinirlari yazilacak:

- neler yapildi
- neler bilerek kapsama alinmadi

### 7. Sistem Mimarisi

Bu bolum raporun kalbi.

Burada su mimari anlatilacak:

`Bus Simulator -> MQTT -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

Bu bolumde:

- genel akisi gosteren bir mimari diyagram
- her katmanin gorevi
- neden bu servislerin secildigi

yazilacak.

### 8. Veri Modeli ve Olay Semasi

Bu bolumde:

- hatlar
- duraklar
- rotalar
- ham event semasi
- bulutta turetilen alanlar

anlatilacak.

Ozellikle su ayrim acik yazilmali:

- simulatorun urettigi `ham veri`
- Lambda'nin hesapladigi `turetilmis veri`

### 9. Gercekleme Ayrintilari

Bu bolum parcalara ayrilmali:

- `Simulator`
- `Processor / Lambda`
- `DynamoDB`
- `FastAPI`
- `Dashboard`

Her alt bolumde su mantik izlenmeli:

- ilgili katman ne yapar
- nasil calisir
- projede nasil kullanildi

### 10. AWS Dagitimi ve Gercek Ortam Dogrulamasi

Bu bolumde:

- IAM Identity Center ile giris
- kullanilan AWS servisleri
- olusturulan kaynaklar
- IoT Core'dan DynamoDB'ye kadar olan canli dogrulama

anlatilacak.

Bu bolum raporu cok guclendirir; cunku sistemin sadece lokal degil, AWS uzerinde de calistigi ispatlanmis olur.

### 11. Sonuclar ve Degerlendirme

Burada:

- sistemin calistigi
- hangi ozelliklerin basarildigi
- hangi sinirlarin oldugu
- gelecekte neler eklenebilecegi

yer alacak.

### 12. Kaynakca

Bu bolumde sadece gercekten kullandigimiz ve metin icinde atif yaptigimiz kaynaklar olmali.

## Hangi Bolume Ne Yazacagiz

Kisa esleme:

- `Giris`: problem ve motivasyon
- `Problem Tanimi`: sentetik veri ve kapsam sinirlari
- `Mimari`: sistem bloklari ve veri akisi
- `Gercekleme`: kod katmanlari ve servisler
- `Degerlendirme`: ne calisti, ne ogrendik, sinirlar

## Raporu Yazma Sirasi

En dogru sira su:

1. `Kapak + Icindekiler iskeleti`
2. `Baslik + Ozet`
3. `Sistem Mimarisi`
4. `Veri Modeli ve Event Semasi`
5. `Gercekleme Ayrintilari`
6. `AWS Dogrulama`
7. `Giris`
8. `Sonuc`
9. `Kaynakca`

Not:

- `Giris` bolumunu en basta yazmak yerine, sistemi anlattiktan sonra yazmak daha kolay olur
- `Ozet` ise her zaman en son parlatilir
- `Icindekiler` otomatik olusturulmali; elle sayfa numarasi yazilmamali

## Rapor Icin Kullanacagimiz Ic Malzeme

Bu repo icindeki belgeler raporu yazarken ana taslak malzeme olacak:

- `docs/specs/architecture.md`
- `docs/specs/data-model.md`
- `docs/specs/data-contract.md`
- `docs/specs/event-schema.md`
- `docs/specs/dynamodb-design.md`
- `docs/specs/api-design.md`
- `docs/specs/dashboard-design.md`
- `docs/specs/aws-environment.md`
- `docs/worklogs/05.04.2026.md`
- `docs/worklogs/19.04.2026.md`

Bu belgeler `kaynakca` icin degil, rapor metnini yazmak icin hammadde olarak kullanilacak.

## Rapor Icin Gerekli Gorseller

Hazirlamamiz gereken gorseller:

- genel sistem mimarisi diyagrami
- dashboard ekran goruntusu
- AWS zincirini gosteren ekran goruntuleri veya tablo
- veri akisini gosteren basit sekil

## Son Yazim Stratejisi

Raporun tonu su olmali:

- akademik ama gereksiz yapay degil
- acik ve savunulabilir
- “hangi teknolojiyi kullandik”tan cok “neden oyle tasarladik” uzerine kurulu

Ana hedef:

`Bu sistemin tasarlandigi, uygulandigi ve AWS uzerinde gercek zamanli calistirildigi acikca gorulmeli.`

## Nihai Format Karari

Son karar:

- `kapak sayfasi olacak`
- `icindekiler olacak`
- teknik ana govde `IEEE-benzeri` duzende yazilacak
- kaynakca `IEEE numarali atif stili` ile verilecek

Yani rapor tipi:

`ders raporu + IEEE-benzeri teknik makale duzeni`
