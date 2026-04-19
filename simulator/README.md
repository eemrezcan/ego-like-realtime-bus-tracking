# Simulator

Bu klasor, sentetik otobus telemetrisi ureten lokal simulatoru tutar.

## Hedef

Bu simulatorun ilk amaci AWS tarafina gecmeden once veri modelinin ve payload yapisinin dogru calistigini gormektir.

## Dosyalar

- `app.py`: CLI giris noktasi
- `data_loader.py`: `data/` altindaki JSON dosyalarini yukler
- `engine.py`: otobuslerin rota uzerinde ilerleme mantigini kurar
- `models.py`: veri modelleri
- `publisher.py`: stdout, dosya veya MQTT yayin katmani
- `local_broker.py`: Docker olmadan venv icinde calisan lokal MQTT broker
- `mqtt_inspector.py`: lokal MQTT akisini dinlemek icin subscriber benzeri arac

## Lokal Calistirma

Dry-run seklinde terminale event akitmak icin:

```powershell
python -m simulator --steps 3 --interval-seconds 3 --no-sleep
```

Eventleri dosyaya yazmak icin:

```powershell
python -m simulator --steps 3 --interval-seconds 3 --output file --file-path output/telemetry.jsonl --no-sleep
```

MQTT cikisi kullanmak icin:

```powershell
python -m simulator --steps 3 --interval-seconds 3 --output mqtt --broker-host localhost --broker-port 1883 --no-sleep
```

Simulatoru kesintisiz calistirmak icin:

```powershell
python -m simulator --continuous --interval-seconds 3 --output mqtt --broker-host localhost --broker-port 1883
```

AWS IoT Core benzeri TLS zorunlu bir broker'a baglanmak icin:

```powershell
python -m simulator --steps 3 --interval-seconds 3 --output mqtt --broker-host <iot-endpoint> --broker-port 8883 --client-id ego-sim-aws --tls --ca-file <AmazonRootCA1.pem> --cert-file <device.pem.crt> --key-file <private.pem.key> --no-sleep
```

AWS uzerinde dashboard'da hareket gormek icin ayni komutu surekli modda calistirmak daha uygundur:

```powershell
python -m simulator --continuous --interval-seconds 3 --output mqtt --broker-host <iot-endpoint> --broker-port 8883 --client-id ego-sim-aws --tls --ca-file <AmazonRootCA1.pem> --cert-file <device.pem.crt> --key-file <private.pem.key>
```

Docker kullanmadan lokal broker baslatmak icin:

```powershell
python -m simulator.local_broker --host 127.0.0.1 --port 1883
```

Inspector ile gelen mesajlari dinlemek icin:

```powershell
python -m simulator.mqtt_inspector --broker-host localhost --broker-port 1883
```

Not:

- MQTT modu icin `paho-mqtt` paketinin kurulu olmasi gerekir
- Ilk dogrulama asamasi icin `stdout` veya `file` modu yeterlidir
- AWS IoT Core'a dogrudan baglanilacaksa genelde `8883` portu ve istemci sertifikasi gerekir
