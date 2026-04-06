# Data Model

Bu belge `data/` klasorundeki dosyalarin ne amacla tasarlandigini aciklar.

## Hedef

Asama 1'in amaci simulator, Lambda ve dashboard'un ayni veri temelini kullanmasini saglamaktir.

Bu nedenle veri modeli sadece durak isimlerinden olusmaz; ayni zamanda rota sirasini ve segment bazli zaman bilgisini de icerir.

## Dosyalar

### `data/lines.json`

Hat bazli metadata tutulur:

- `line_id`
- `public_code`
- `name`
- `vehicle_capacity`
- `nominal_headway_seconds`
- `service_start`
- `service_end`

Bu dosya daha sonra simulator tarafinda arac olusturma ve dashboard tarafinda hat ozetleri icin kullanilacaktir.

### `data/stops.json`

Durak bazli referans veri tutulur:

- `stop_id`
- `name`
- `district`
- `lat`
- `lon`
- `stop_type`
- `activity_tags`

`stop_type` ve `activity_tags`, ileride `estimated_alighting_count` ve `boarding_count` davranisini kurallarla zenginlestirmek icin secilmistir.

### `data/routes.json`

Hatlarin kanonik durak sirasi ve segment bilgileri tutulur:

- `stop_sequence`
- `segments`
- `default_dwell_seconds`
- `default_terminal_wait_seconds`

Bu dosya su islerde kullanilacaktir:

- simulatorun otobusu rota uzerinde ilerletmesi
- sonraki duragin bulunmasi
- ETA hesaplamasi
- gecikme mantigi icin referans seyahat suresi kullanimi

## Secilen Hatlar

Veri modeli uc hat ile sinirlandirildi:

- `LINE_510`: Kizilay - Sogutozu
- `LINE_520`: Ulus - Dikimevi
- `LINE_530`: Kizilay - Bilkent Koprusu

Bu secim su dengeyi saglar:

- Ankara merkezini andiran bir ag yapisi
- Ortak transfer dugumleri
- Haritada anlasilir bir dagilim
- Asiri buyumeyen MVP kapsami

## Tasarim Ilkeleri

- Her hat icin tek bir kanonik rota tutulur
- Ters yon, ayni rotanin ters cevrilmesiyle elde edilir
- Koordinatlar gercege yakin ama simule edilmeye uygun degerlerdir
- Veri modeli, tek seferlik demo degil sonraki asamalari da destekleyecek sekilde kurulmustur
