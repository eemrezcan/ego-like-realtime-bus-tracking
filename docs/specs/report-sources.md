# Rapor Kaynak Plani

Bu belge, final raporda hangi kaynaklarin kullanilacagini ve bu kaynaklarin hangi bolumlerde ise yarayacagini netlestirir.

## Temel Ilke

Rapor icinde iki tur malzeme kullanacagiz:

1. `Dis kaynaklar`
   Bunlar kaynakca bolumunde yer alacak resmi veya akademik referanslardir.

2. `Ic proje kayitlari`
   Bunlar repodaki dokumanlarimiz, worklog'larimiz ve kod yapimizdir.
   Bunlar raporu yazarken kullanilir ama normalde `kaynakca`ya yazilmaz.

## Onerilen Dis Kaynaklar

Asagidaki kaynaklar su an icin ana referans setimiz olacak.

### A. Bicim Kaynagi

1. `IEEE Conference Template`
   Kullanım amacı:
   IEEE-benzeri iki sutunlu rapor formatini kurmak.

### B. Protokol ve Iletisim

2. `MQTT Version 3.1.1 (OASIS Standard)`
   Kullanim amaci:
   MQTT'nin publish/subscribe mantigini ve hafif bir IoT mesajlasma protokolu oldugunu temellendirmek.

3. `AWS IoT Core MQTT`
   Kullanim amaci:
   AWS IoT Core'un MQTT destegini ve cihaz-bulut iletisim katmanini aciklamak.

4. `Rules for AWS IoT`
   Kullanim amaci:
   MQTT ile gelen verinin AWS servislerine kural tabanli yonlendirilmesini aciklamak.

### C. Gercek Zamanli Veri Isleme

5. `Amazon Kinesis Data Streams`
   Kullanim amaci:
   neden gercek zamanli veri yutma ve isleme hattinda Kinesis kullanildigini aciklamak.

6. `Using Lambda to process records from Amazon Kinesis Data Streams`
   Kullanim amaci:
   Kinesis'ten gelen verinin Lambda ile nasil tuketildigini ve islendigi yapinin gerekcesini vermek.

### D. Depolama

7. `Amazon DynamoDB`
   Kullanim amaci:
   anlik bus durumu ve gecmis telemetri kayitlari icin secilen veritabanini aciklamak.

### E. Sunum Katmani

8. `FastAPI First Steps`
   Kullanim amaci:
   okuma API'si katmaninin neden ve nasil kurgulandigini desteklemek.

9. `Streamlit st.pydeck_chart`
   Kullanim amaci:
   dashboard ve harita gorsellestirmesinin teknik temelini belirtmek.

## Bu Kaynaklari Hangi Bolumde Kullanacagiz

### Giris

Kullanilabilecek kaynaklar:

- MQTT standardi
- AWS IoT Core MQTT
- Kinesis Data Streams

Burada “gercek zamanli veri akisi” ve “hafif cihaz protokolu” fikri desteklenir.

### Sistem Mimarisi

Kullanilacak kaynaklar:

- AWS IoT Rules
- Kinesis Data Streams
- AWS Lambda with Kinesis
- DynamoDB

Bu bolumde mimarideki her AWS katmaninin resmi dayanaklari olur.

### Gercekleme Ayrintilari

Kullanilabilecek kaynaklar:

- FastAPI docs
- Streamlit docs

Bu kaynaklar arayuz ve API katmanini destekler.

### Bicim / Sunum

Kullanilacak kaynak:

- IEEE Conference Template

Bu kaynak metnin format secimi icin gerekir; proje teknik icerigini desteklemez ama sunum bicimini aciklar.

## Ic Proje Kayitlarindan Ne Cekilecek

Asagidaki belgeler raporun yazim malzemesidir:

- `docs/decisions/001-proje-vizyonu.md`
- `docs/decisions/002-mvp-kapsami.md`
- `docs/decisions/003-teknik-yigin.md`
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

Bu belgelerden cekilecek bilgi turleri:

- mimari anlatim
- veri semasi
- AWS ortam kurulumu
- test ve dogrulama adimlari
- alinan teknik kararlarin gerekceleri

## Kaynakca Icin Onerilen Asgari Liste

Raporun sonunda en az su kaynaklarin olmasi yeterli ve guclu olur:

1. IEEE Conference Template
2. MQTT Version 3.1.1 OASIS Standard
3. AWS IoT Core MQTT
4. AWS IoT Rules
5. Amazon Kinesis Data Streams
6. AWS Lambda with Kinesis Data Streams
7. Amazon DynamoDB
8. FastAPI official docs
9. Streamlit official docs

Bu liste teknik olarak yeterli. Daha akademik gorunmesini istersek sonraki asamada `2-3` adet toplu tasima, IoT veya gercek zamanli izleme konulu makale ekleyebiliriz.

## Onerilen Atif Stratejisi

Asiri atif kullanmayacagiz. Atiflar sunlar icin kullanilacak:

- MQTT neden uygun?
- AWS servisleri neden bu akista mantikli?
- DynamoDB neden secildi?
- Dashboard ve API katmani neye dayanarak kuruldu?

Yani her paragrafta atif degil; `gerekce gerektiren` paragraflarda atif.

## Bu Asamada Net Karar

Su an rapor icin resmi kaynak setimiz:

- `IEEE resmi template`
- `OASIS MQTT standardi`
- `AWS resmi dokumantasyonu`
- `FastAPI resmi dokumantasyonu`
- `Streamlit resmi dokumantasyonu`

Bir sonraki asamada istersek buna `akademik literatur` katmani ekleriz.
