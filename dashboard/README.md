# Dashboard

Bu klasor, Streamlit ile gelistirilen canli izleme ekranini tutar.

## Hedef

API katmanindan gelen anlik durum bilgisini gorsel olarak sunmak.

Dashboard su bolumleri gosterir:

- sistem durumu banner'i
- genel ozet kartlari
- canli harita
- otobus tablosu
- hat bazli ozet kartlari
- secili otobus detay paneli

## Veri Kaynagi

Dashboard dogrudan veritabanina baglanmaz.

Kaynak:

- FastAPI okuma katmani

## Lokal Calistirma

1. Zenginlestirilmis event dosyasini uret:

```powershell
.\.venv\Scripts\python.exe -m simulator --steps 2 --interval-seconds 3 --output file --file-path output/telemetry.jsonl --no-sleep
.\.venv\Scripts\python.exe -m processor --input-file output/telemetry.jsonl --output-file output/enriched-telemetry.jsonl
```

2. API'yi baslat:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

3. Dashboard'u baslat:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

## Ortam Degiskenleri

- `DASHBOARD_API_BASE_URL=http://127.0.0.1:8000`
- `DASHBOARD_DEFAULT_LINE=`
- `DASHBOARD_AUTO_REFRESH_SECONDS=5`

## Canli Hareket Notu

Dashboard kendi basina veri uretmez; sadece API uzerinden gelen son durumu gosterir.

Bu nedenle haritadaki otobuslerin hareket etmesi icin simulatorun surekli veri gonderiyor olmasi gerekir.

Onerilen canli akis:

```powershell
.\.venv\Scripts\python.exe -m simulator --continuous --interval-seconds 3 --output mqtt --broker-host <iot-endpoint> --broker-port 8883 --client-id ego-sim-aws --tls --ca-file <AmazonRootCA1.pem> --cert-file <device.pem.crt> --key-file <private.pem.key>
```

Bu komut acik kaldigi surece dashboard varsayilan olarak her 5 saniyede bir yenilenir ve haritadaki noktalar guncellenir.

## AWS Verisi Ile Calistirma

Eger API katmani `dynamodb` modunda ayaga kaldirildiysa dashboard ayni sekilde bu gercek AWS verisini gosterebilir.

Ornek akış:

1. API'yi AWS verisi ile baslat:

```powershell
$env:AWS_PROFILE='eemrezcan'
$env:API_STORAGE_MODE='dynamodb'
$env:AWS_REGION='eu-central-1'
$env:DDB_CURRENT_STATE_TABLE='bus_current_state'
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8011
```

2. Dashboard'u bu API'ye bagla:

```powershell
$env:DASHBOARD_API_BASE_URL='http://127.0.0.1:8011'
$env:DASHBOARD_AUTO_REFRESH_SECONDS='5'
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py --server.port 8511
```

Bu modda dashboard, `bus_current_state` tablosundaki gercek AWS verisini FastAPI uzerinden gosterir.
