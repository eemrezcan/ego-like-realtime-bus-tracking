# API

Bu klasor dashboard'un okuyacagi FastAPI tabanli okuma katmanini tutar.

## Hedef

Dashboard'un dogrudan veritabanina baglanmasi yerine API uzerinden veri cekmesi.

Bu katman su endpointleri saglar:

- `GET /health`
- `GET /buses`
- `GET /buses/{bus_id}`
- `GET /lines`
- `GET /summary`

## Storage Modlari

### `jsonl`

Lokal gelistirme icin. Varsayilan mod budur.

Kaynak dosya:

- `output/enriched-telemetry.jsonl`

### `dynamodb`

AWS ortami icin.

Kaynak:

- `bus_current_state` tablosu

## Lokal Calistirma

1. Ham event dosyasi uret:

```powershell
.\.venv\Scripts\python.exe -m simulator --steps 2 --interval-seconds 3 --output file --file-path output/telemetry.jsonl --no-sleep
```

2. Zenginlestirilmis event dosyasi uret:

```powershell
.\.venv\Scripts\python.exe -m processor --input-file output/telemetry.jsonl --output-file output/enriched-telemetry.jsonl
```

3. API'yi baslat:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

## Ortam Degiskenleri

- `API_STORAGE_MODE=jsonl`
- `API_ENRICHED_EVENTS_FILE=output/enriched-telemetry.jsonl`

AWS tarafinda:

- `API_STORAGE_MODE=dynamodb`
- `AWS_PROFILE=<profil>` yerel gelistirmede istege bagli ama tavsiye edilir
- `AWS_REGION=<bolge>`
- `DDB_CURRENT_STATE_TABLE=bus_current_state`
- `DDB_ENDPOINT_URL=` istege bagli
