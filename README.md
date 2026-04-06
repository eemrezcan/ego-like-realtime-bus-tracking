# EGO-Like Realtime Bus Tracking

Bu repo, `EGO-benzeri sentetik veri ile gercek zamanli otobus takip ve yogunluk analiz sistemi` projesini icerir.

Projede sentetik otobus telemetrisi uretilir, MQTT uzerinden akan veri islenir, zenginlestirilir ve canli dashboard uzerinden gosterilir.

## Mimari

Temel hedef mimarisi:

`Bus Simulator -> MQTT -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

Yerel gelistirme akisinda dosya bazli ve lokal broker bazli prova desteklenir.

## Proje Yapisi

- `data/`: Hat, durak ve rota tanimlari
- `schemas/`: Resmi veri semalari
- `simulator/`: Sentetik telemetri uretimi
- `processor/`: ETA, yogunluk ve gecikme hesaplamalari
- `api/`: Okuma katmani
- `dashboard/`: Streamlit arayuzu
- `docs/`: Kararlar, teknik notlar ve gunluk calisma kayitlari

## Yerel Kurulum

Sanal ortam:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Lokal MQTT broker:

```powershell
docker compose -f docker-compose.local.yml up --build -d
```

## Yerel Calistirma

Ham telemetri uret:

```powershell
.\.venv\Scripts\python.exe -m simulator --steps 2 --interval-seconds 3 --output file --file-path output/telemetry.jsonl --no-sleep
```

Veriyi zenginlestir:

```powershell
.\.venv\Scripts\python.exe -m processor --input-file output/telemetry.jsonl --output-file output/enriched-telemetry.jsonl
```

API'yi baslat:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Dashboard'u ac:

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard/app.py
```

## Dokumantasyon

Baslangic icin:

- `docs/README.md`
- `docs/planning/implementation-roadmap.md`
- `docs/worklogs/05.04.2026.md`
