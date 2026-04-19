# EGO-Like Realtime Bus Tracking

Bu repo, `EGO-benzeri sentetik veri ile gerçek zamanlı otobüs takip ve yoğunluk analiz sistemi` projesinin final çalışma kopyasını içerir. Sistem, sentetik otobüs telemetrisi üretir; bu veriyi MQTT üzerinden AWS hattına taşır, bulutta işler ve canlı dashboard üzerinde gösterir.

## Temel Mimari

`Simulator -> MQTT -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

Bu yapı hem yerel geliştirme akışında hem de AWS üzerinde uçtan uca doğrulanmıştır.

## Repoda Neler Var

- `final-report.pdf`: hocaya gösterilecek hazır final raporu
- `report/`: raporun kaynak dosyaları, LaTeX taslağı ve PDF üretim scripti
- `simulator/`: sentetik otobüs telemetrisi üreten katman
- `processor/`: ETA, tahmini iniş, doluluk ve gecikme hesapları
- `api/`: DynamoDB veya yerel veri kaynağından okuyan FastAPI katmanı
- `dashboard/`: Streamlit tabanlı canlı izleme arayüzü
- `data/`: hat, durak ve rota tanımları
- `schemas/`: veri sözleşmeleri ve event şemaları
- `infra/`: AWS ve yerel altyapı scriptleri
- `docs/`: karar kayıtları, teknik notlar, günlükler ve planlar
- `tests/`: temel birim testleri
- `silinebilecekler/`: repoda tutulmayan veya geçici üretilen dosyalarla ilgili notlar

## Hızlı Başlangıç

Bağımlılık kurulumu:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Testler:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_processor tests.test_api_service tests.test_dashboard_view_models
```

Yerel API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Dashboard:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

## Rapor

Hazır PDF doğrudan kökte bulunur:

- `final-report.pdf`

Rapor kaynak dosyaları:

- `report/main.tex`
- `report/REPORT_PREVIEW.md`
- `report/build_report_pdf.py`

PDF yeniden üretmek için:

```powershell
.\.venv\Scripts\python.exe report/build_report_pdf.py
```

## AWS Doğrulama

Projede şu zincir çalışır durumda kurulmuştur:

`Simulator -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

AWS kurulum ve doğrulama notları için:

- `docs/specs/aws-environment.md`
- `infra/aws/README.md`

## Dokümantasyon

Başlangıç için en iyi giriş noktaları:

- `docs/README.md`
- `docs/planning/implementation-roadmap.md`
- `docs/planning/report-roadmap.md`
- `docs/worklogs/05.04.2026.md`

## Not

Geçici çıktı klasörleri, yerel loglar, Lambda paketleri ve AWS cihaz sertifikaları repoda tutulmamaktadır. Bunların özeti `silinebilecekler/README.md` içinde bırakılmıştır.
