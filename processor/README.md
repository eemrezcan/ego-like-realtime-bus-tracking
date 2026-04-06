# Processor

Bu klasor, simulator tarafindan uretilen ham telemetri eventlerini zenginlestiren isleme katmanini tutar.

## Hedef

Bu katmanin amaci ham eventten su alanlari uretmektir:

- `estimated_eta_sec`
- `estimated_alighting_count`
- `estimated_occupancy_score`
- `estimated_occupancy_level`
- `is_delayed`

Bu mantik Lambda tarafina tasinabilecek sekilde yazildi, ancak lokalde de denenebilir.

## Dosyalar

- `validators.py`: ham event dogrulama ve parse islemleri
- `eta.py`: mesafe ve hiz tabanli ETA mantigi
- `occupancy.py`: inis tahmini ve doluluk hesaplari
- `config.py`: storage modu ve DynamoDB ayarlari
- `repository.py`: memory ve DynamoDB repository katmani
- `service.py`: ana zenginlestirme akisi
- `lambda_handler.py`: AWS Lambda uyumlu giris noktasi
- `local_runner.py`: dosyadan gelen eventleri lokalde isleyen CLI

## Lokal Kullanim

Simulator output dosyasini islemek icin:

```powershell
.\.venv\Scripts\python.exe -m processor --input-file output/telemetry.jsonl
```

## Tasarim Notlari

- Processor, ham event ile turetilmis event arasindaki ayirimi korur
- Doluluk tahmini onceki durum + binen - tahmini inen mantigiyla ilerler
- Gecikme durumu planlanan kalan sure ile tahmini kalan sure arasindaki farka gore belirlenir
- Repository modu `memory` veya `dynamodb` olabilir
- Lambda icinde ayni is mantigi kullanilir, sadece repository degisir
