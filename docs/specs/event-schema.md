# Event Schema

Bu belge `event schema` ifadesinin projedeki anlamini ve neden erken asamada donduruldugunu aciklar.

## Event Schema Ne Demek

Event schema, sistemde akan tek bir mesajin resmi yapisidir.

Baska bir ifadeyle su sorularin tek cevabidir:

- Mesaj hangi alanlari tasir
- Alanlarin adlari nedir
- Her alanin veri tipi nedir
- Hangi alanlar zorunludur
- Hangi format ve sinirlar gecerlidir

Bu projede event schema, simulatorun MQTT ile gonderecegi ham telemetri olayini tanimlar.

## Neden Simdi Yapiyoruz

Schema dondurulmadan bir sonraki asamalar dagilmaya baslar.

Ornek sorunlar:

- Simulator `speed` gonderir, Lambda `speed_kmh` bekler
- Biri `next_stop`, digeri `next_stop_id` kullanir
- Dashboard `boarding_count` yerine baska bir alan arar

Schema dosyasi bu daginikligi engeller.

## Bu Repo Icindeki Karsiligi

Makine tarafindan okunabilir resmi schema dosyasi:

- `schemas/bus-telemetry.schema.json`

Insan tarafindan okunabilir baglam:

- `docs/specs/data-contract.md`

Bu iki belge birlikte okunmalidir:

- `data-contract.md` neyi neden tasidigimizi anlatir
- `bus-telemetry.schema.json` ise formatin tam kurallarini sabitler

## Dondurulmus Ham Event

Bu projede simulatorun gonderecegi ham event alanlari sunlardir:

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

## Neden Bu Alanlar Var

- `event_id`: tekil mesaj takibi icin
- `timestamp`: zaman ekseni uzerinde analiz icin
- `bus_id`: araca gore ayrim icin
- `line_id`: hat bazli analiz icin
- `route_direction`: gidis ve donus ayrimi icin
- `lat`, `lon`: canli konum icin
- `speed_kmh`: ETA ve gecikme icin
- `next_stop_id`, `next_stop_name`: bir sonraki durak baglami icin
- `boarding_count`: kart basimindan gelen tek dogrudan yolcu sinyali icin

## Neyi Bilerek Ham Evente Koymadik

- `estimated_eta_sec`
- `estimated_alighting_count`
- `estimated_occupancy_score`
- `estimated_occupancy_level`
- `is_delayed`

Bu alanlar bulutta hesaplanacak. Boylece proje sadece veri gosteren degil, veri isleyen bir sistem olur.

## Dondurmak Ne Demek

Buradaki "dondurmak" su anlama gelir:

- Bundan sonra alan adlarini keyfi degistirmiyoruz
- Veri tiplerini keyfi degistirmiyoruz
- Yeni alan eklersek once schema ve docs guncelleniyor
- Sonra kod degisiyor

Bu kural repo disiplininin bir parcasi olacak.
