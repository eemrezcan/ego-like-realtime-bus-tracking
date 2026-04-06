# Dependencies

Bu belge projede kullanilacak Python paketlerini ve sabitlenen surumlerini listeler.

## Ilke

Bu projede bagimliliklar "floating" birakilmayacak, belirli surumlere sabitlenecektir.

Ana sebep:

- ekip ici tekrar uretilebilirlik
- ayni davranisi farkli makinelerde korumak
- demo gununde surpriz kirilimlari azaltmak

## Runtime Bagimliliklari

### `boto3==1.42.66`

AWS servisleriyle Python uzerinden etkilesim kurmak icin.

Kullanilacagi yerler:

- DynamoDB erisimi
- IoT Core ve diger AWS servis entegrasyonlari

### `python-dotenv==1.2.2`

Lokal gelistirme sirasinda ortam degiskenlerini `.env` dosyasindan yuklemek icin.

Kullanilacagi yerler:

- AWS kimlik bilgileri disindaki proje ayarlari
- lokal broker veya API konfigurasyonu

### `requests==2.33.1`

FastAPI katmanindan dashboard tarafina veri cekmek icin.

Kullanilacagi yerler:

- dashboard API istemcisi
- health, summary, lines ve buses endpoint cagirilari

### `paho-mqtt==2.1.0`

MQTT istemcisi olarak kullanilacak.

Kullanilacagi yerler:

- simulatorun MQTT broker'a veri gondermesi
- lokal MQTT testleri

### `amqtt==0.11.3`

Venv icinde calisan lokal MQTT broker fallback'i icin.

Kullanilacagi yerler:

- Docker Desktop kapaliyken yerel broker testi
- `simulator -> broker -> inspector` provasini lokal olarak tamamlamak

### `fastapi==0.135.2`

Dashboard'a veri saglayacak okuma API katmani icin.

### `uvicorn==0.41.0`

FastAPI uygulamasini lokal gelistirme sirasinda calistirmak icin ASGI sunucusu.

### `streamlit==1.55.0`

Canli dashboard arayuzu icin.

## Kurulum

Sanal ortam aktif edilmeden de dogrudan venv yorumlayicisi ile kurulabilir:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Not

Su an bu bagimliliklar repoya eklendi, ancak kurulum komutu otomatik olarak calistirilmadi.
