# Dashboard Design

Bu belge Streamlit dashboard'un neyi gosterdigini ve neden bu sekilde tasarlandigini aciklar.

## Tasarim Amaci

Dashboard sadece tablo gostermek icin degil, demonstrasyon sirasinda projenin uc farkli yonunu ayni anda gostermek icin tasarlandi:

- veri akiyor mu
- araclarin anlik durumu ne
- analiz katmani ne urett i

## Ekran Bolumleri

### Durum Banner'i

Sistemin genel sagligini ve storage modunu gosterir.

### Ozet Kartlari

- toplam otobus
- ortalama hiz
- geciken arac sayisi
- yuksek doluluk sayisi

### Harita

Canli konumlari tek ekranda gormek icin.

### Otobus Tablosu

Dashboard'un en dogrudan operasyonel gorunumudur.

### Hat Ozet Kartlari

Her hattin aktif arac sayisi, ortalama hiz ve ETA durumunu karsilastirmayi kolaylastirir.

### Secili Otobus Detayi

Tek bir otobusun ETA, hiz, binis ve tahmini inis bilgisini odakli gosterir.

## Neden API Uzerinden Besleniyor

- dashboard veritabanindan bagimsiz kalir
- lokal gelistirme kolaylasir
- AWS tarafina gectigimizde ekran kodu degismez
