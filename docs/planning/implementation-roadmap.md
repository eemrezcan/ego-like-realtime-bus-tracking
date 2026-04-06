# Uygulama Sirasi

Bu belge "nereden baslayacagiz?" sorusunun tek kaynak cevabidir.

## Temel Cevap

Projeye altyapi kurarak degil, veri modelini dondurarak baslanacaktir.

## Asama 0: Dokumani Dondur

Ilk olarak asagidaki maddeler onaylanmis olmalidir:

- Proje vizyonu
- MVP kapsami
- Teknik yigin
- Ham veri ve turetilmis veri ayrimi

Bu dort madde onaylanmadan gelistirmeye gecilmez.

## Asama 1: Veri Modeli

Ilk teknik is su olacaktir:

- Hat listesi
- Durak listesi
- Hat-durak iliskileri
- MQTT event yapisi

Bu asamanin ciktisi:

- `data/lines.json`
- `data/stops.json`
- `data/routes.json`

## Asama 2: Lokal Simulasyon

- Python ile bus simulator yazilir
- MQTT mesajlari lokal ortamda uretilir
- Event formatinin dogru calistigi gorulur

Bu asamada AWS tarafina gecmeden once veri akisi lokal olarak test edilir.

## Asama 3: AWS Veri Hatti

- AWS IoT Core MQTT girisi kurulur
- IoT Rule ile Kinesis baglantisi yapilir
- Lambda isleme fonksiyonu eklenir
- DynamoDB tablolari olusturulur

## Asama 4: Okuma Katmani

- FastAPI ile veri okuma endpoint'leri yazilir
- Anlik durum ve ozet veriler sunulur

## Asama 5: Dashboard

- Streamlit ekrani olusturulur
- Otobus listesi, gecikme, ETA ve yogunluk gosterilir
- Harita ilk surumde sade tutulur

## Asama 6: Rapor ve Video Hazirligi

- Ekran goruntuleri ve mimari diyagram eklenir
- Git commit gecmisi duzenli hale getirilir
- Demo senaryosu cikarilir

## Ilk Pratik Gorevler

Bu depoda bundan sonra ilk yapilacaklar:

1. `data/` klasorundeki hat ve durak JSON dosyalarini olusturmak
2. `simulator/` icin temel Python iskeletini kurmak
3. MQTT payload'ini uretecek modeli yazmak

## Bir Sonraki Karar Kurali

Yeni bir teknik detay tartisilirken once su soru sorulur:

`Bu karar MVP'yi sadelestiriyor mu, yoksa gereksiz karmasiklastiriyor mu?`
