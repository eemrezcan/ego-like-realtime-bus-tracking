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
