# Mimari

## Ust Duzey Akis

`Bus Simulator -> MQTT -> AWS IoT Core -> IoT Rule -> Kinesis Data Streams -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

## Bilesenler

### 1. Bus Simulator

- Sentetik otobus verisi uretir
- Belirli araliklarla MQTT mesajlari gonderir
- Sadece ham veri uretir

### 2. AWS IoT Core

- MQTT mesajlarini kabul eder
- Giris noktasi gorevi gorur

### 3. AWS IoT Rule

- IoT Core'a gelen mesajlari Kinesis'e yonlendirir

### 4. Kinesis Data Streams

- Gelen veriyi akis halinde tasir
- Gercek zamanli veri isleme hattinin omurgasini olusturur

### 5. AWS Lambda

- Gelen ham veriyi isler
- ETA ve yogunluk gibi turetilmis alanlari hesaplar
- Sonucu DynamoDB'ye yazar

### 6. DynamoDB

- `bus_current_state` tablosunda son durumu tutar
- `telemetry_history` tablosunda gecmisi tutar
- Processor repository katmani uzerinden yazilir

### 7. FastAPI

- Dashboard'un tukecegi okuma API'lerini saglar
- DynamoDB'den veri ceker

### 8. Streamlit Dashboard

- Canli durum ekranidir
- Harita, tablo ve ozet kartlari gosterir

## Mimari Ilkeler

- Ham veri ile turetilmis veri ayri tutulur
- Simulasyon ve analiz mantigi ayni kod parcasi icinde karistirilmaz
- Gosterim katmani dogrudan MQTT'den degil API veya veritabani katmanindan beslenir
- Ilk hedef calisan bir veri akisidir; gorsel detaylar ikinci asamadadir
