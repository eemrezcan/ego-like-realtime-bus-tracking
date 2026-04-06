# DynamoDB Design

Bu belge Lambda sonrasi yazma katmaninin DynamoDB uzerindeki tasarimini aciklar.

## Hedef

Processor tarafinda uretilen zenginlestirilmis event iki farkli saklama ihtiyacina hizmet eder:

- her otobusun son durumunu hizli okumak
- gecmis telemetriyi analiz icin saklamak

Bu nedenle iki tablo kullanilir.

## Tablo 1: `bus_current_state`

Amaci:

- dashboard'un canli ekrani
- her otobus icin en son bilinen durum

Anahtar yapisi:

- Partition key: `bus_id`

Tutulan alanlar:

- `bus_id`
- `timestamp`
- `event_id`
- `line_id`
- `route_direction`
- `lat`
- `lon`
- `speed_kmh`
- `next_stop_id`
- `next_stop_name`
- `boarding_count`
- `estimated_eta_sec`
- `estimated_alighting_count`
- `estimated_occupancy_score`
- `estimated_occupancy_level`
- `is_delayed`

## Tablo 2: `telemetry_history`

Amaci:

- gecmise donuk inceleme
- rapor ve demo verisi
- analiz ve ozet sorgulari

Anahtar yapisi:

- Partition key: `bus_id`
- Sort key: `timestamp`

Tutulan alanlar:

- ham event alanlari
- turetilmis tum alanlar

## Neden Iki Tablo

Tek tabloda da tutulabilir, ancak bu MVP icin iki tablo daha acik ve daha savunulabilir:

- `bus_current_state` canli okumayi kolaylastirir
- `telemetry_history` zaman serisi incelemeyi ayirir

## Processor Baglami

Processor repository katmani iki modda calisir:

- `memory`: lokal gelistirme
- `dynamodb`: AWS yazma modu

Bu mod `PROCESSOR_STORAGE_MODE` ortam degiskeni ile secilir.

## Gerekli Ortam Degiskenleri

- `PROCESSOR_STORAGE_MODE=dynamodb`
- `AWS_REGION=<bolge>`
- `DDB_CURRENT_STATE_TABLE=bus_current_state`
- `DDB_HISTORY_TABLE=telemetry_history`

Istege bagli:

- `DDB_ENDPOINT_URL` -> DynamoDB Local gibi durumlar icin
