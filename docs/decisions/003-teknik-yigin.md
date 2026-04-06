# Karar 003: Teknik Yigin

## Karar Ozeti

Proje asagidaki teknik yigin ile gelistirilecektir:

- Dil: `Python`
- Protokol: `MQTT`
- Bulut: `AWS`
- MQTT girisi: `AWS IoT Core`
- Veri akisi: `AWS IoT Core Rule -> Kinesis Data Streams`
- Isleme: `AWS Lambda`
- Veritabani: `DynamoDB`
- API: `FastAPI`
- Dashboard: `Streamlit`

## Neden Bu Yigin

### Python

- Simulasyon, veri isleme ve AWS SDK kullanimi icin hizlidir
- Rapor ve demo icin ogrenme egrisi dusuktur

### MQTT

- Otobus telemetrisi ve cihaz benzeri veri akisina dogal oturur
- Publish/subscribe yapisi bu senaryo icin uygundur

### AWS

- Ders metnindeki AWS ornek akisiyla uyumludur
- Kinesis, Lambda ve DynamoDB tek platform icinde calisir

### DynamoDB

- AWS ile dogal entegre olur
- Uctan uca teslim riskini azaltir
- Canli durum ve gecmis kayitlar icin yeterlidir

## Degerlendirilen Ama Secilmeyen Alternatifler

### InfluxDB

- Telemetri ve zaman serisi verisi icin cok uygun bir alternatiftir
- Ancak MVP icin ek servis yonetimi ve entegrasyon yuku getirdigi icin ilk tercih edilmemistir

### MongoDB

- Esnek bir belge veritabanidir
- Bu proje icin DynamoDB'ye gore belirgin bir avantaj sunmamaktadir

### Redis

- Hizli ve faydali bir yardimci katman olabilir
- Ancak MVP icin ana veritabani olarak gerekli gorulmemistir

## Sonuc

Bu proje icin "en alan-dogal veritabani" ile "en dengeli teslim mimarisi" ayni sey degildir. MVP'de teslim riski dusuk ve AWS ile butunlesik oldugu icin DynamoDB tercih edilmistir.
