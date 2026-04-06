# Veri Sozlesmesi

Bu belge projenin en kritik baslangic noktasi olarak kabul edilir.

Kod yazimina gecmeden once su ayrim sabitlenmelidir:

- Simulatorden gelen veri `ham veri`
- AWS tarafinda hesaplanan veri `turetilmis veri`

## Dondurulmus Ilke

`Otobus simulasyonu sadece dogrudan gozlenebilir ham veriyi gonderir. ETA, tahmini inis, tahmini doluluk ve gecikme bilgisi bulutta hesaplanir.`

## Ham Veri Alanlari

Simulatorden MQTT ile gonderilecek alanlar:

- `event_id`
- `timestamp`
- `bus_id`
- `line_id`
- `route_direction`
- `lat`
- `lon`
- `speed_kmh`
- `next_stop_id`
- `next_stop_name`
- `boarding_count`

## Neden `alighting_count` Ham Veri Degil

Bu projede kart basim verisi sadece binis davranisini temsil eder. Inis davranisi dogrudan gozlenmedigi icin ham veri olarak gonderilmeyecektir. Bunun yerine bulut tarafinda tahmin edilecektir.

## Bulutta Hesaplanacak Alanlar

- `estimated_eta_sec`
- `estimated_alighting_count`
- `estimated_occupancy_score`
- `estimated_occupancy_level`
- `is_delayed`

## MQTT Topic

Ilk surumde tek topic kullanilacaktir:

`ego-sim/v1/bus/telemetry`

## Ornek Event

```json
{
  "event_id": "0d5d7d84-9d55-4b4e-9f92-8b7d0f3d1a11",
  "timestamp": "2026-04-06T14:30:00Z",
  "bus_id": "BUS_101",
  "line_id": "LINE_510",
  "route_direction": "outbound",
  "lat": 39.92077,
  "lon": 32.85411,
  "speed_kmh": 34.2,
  "next_stop_id": "STOP_12",
  "next_stop_name": "Kizilay",
  "boarding_count": 3
}
```

## Tahmin Mantigi

Ilk surumde basit ama savunulabilir kurallar kullanilacaktir:

- `estimated_eta_sec`: mesafe ve hiz bilgisinden hesaplanir
- `estimated_alighting_count`: duragin hattaki konumu, onceki doluluk ve basit kural seti ile tahmin edilir
- `estimated_occupancy_score`: onceki doluluk + binen - tahmini inen mantigi ile hesaplanir
- `estimated_occupancy_level`: skor araligina gore `dusuk`, `orta`, `yuksek` olarak siniflanir
- `is_delayed`: beklenen ve hesaplanan varis davranisina gore belirlenir

## DynamoDB Tablolari

### `bus_current_state`

Her otobus icin yalnizca en guncel durum tutulur.

Amaci:

- Dashboard'u hizli beslemek
- Her otobusun "su anki" durumunu gostermek

### `telemetry_history`

Telemetri ve turetilmis alanlar gecmis kayit olarak tutulur.

Amaci:

- Analiz yapmak
- Rapor ve demo verisi saklamak
- Gecmise donuk sorgu yapmak
