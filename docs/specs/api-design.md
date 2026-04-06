# API Design

Bu belge FastAPI okuma katmaninin sorumluluklarini aciklar.

## Neden API Katmani Var

Dashboard'un dogrudan DynamoDB'ye baglanmasi yerine API uzerinden veri cekmesi daha temizdir.

Avantajlari:

- veri erisim mantigi tek yerde toplanir
- dashboard sade kalir
- storage degisse bile arayuz ayni kalir
- lokal gelistirme daha kolay olur

## Endpointler

### `GET /health`

Sistemin temel durumu ve aktif storage modunu dondurur.

### `GET /buses`

Tum otobuslerin anlik durumunu dondurur.

### `GET /buses/{bus_id}`

Tek bir otobusun anlik durumunu dondurur.

### `GET /lines`

Hat bazli toplu ozet uretir:

- aktif arac sayisi
- ortalama hiz
- ortalama ETA
- geciken arac sayisi
- yogunluk dagilimi

### `GET /summary`

Sistemin genel ozetini dondurur.

## Storage Modlari

- `jsonl`: lokal gelistirme
- `dynamodb`: AWS ortami

Bu sayede ayni API sozlesmesi korunur, sadece veri kaynagi degisir.
