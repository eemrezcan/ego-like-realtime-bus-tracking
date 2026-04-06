# Lokal Broker Kurulumu

Bu belge lokal MQTT broker'in repo icinde nasil ayaga kaldirilacagini anlatir.

## Secilen Yontem

Lokal test ortami icin Docker Compose ile `Eclipse Mosquitto` broker kullanilir.

Bu secim su sebeplerle yapildi:

- hizli kurulum
- platformlar arasi tutarli davranis
- ekstra lokal servis kurulumu gerektirmemesi
- MQTT icin standart ve hafif bir broker olmasi

## Alternatif Yontem

Docker Desktop kapaliysa veya engine calismiyorsa, Python tabanli fallback broker kullanilabilir:

```powershell
.\.venv\Scripts\python.exe -m simulator.local_broker --host 127.0.0.1 --port 1883
```

Bu fallback, `amqtt` paketinin broker API'sini kullanir.

## Dosyalar

- `docker-compose.local.yml`
- `infra/local/mosquitto/config/mosquitto.conf`

## Baslatma

```powershell
docker compose -f docker-compose.local.yml config
docker compose -f docker-compose.local.yml up --build -d
docker compose -f docker-compose.local.yml ps
```

## Beklenen Sonuc

`mqtt-broker` servisinin ayakta gorunmesi gerekir ve host makinede `1883` portu acik olur.

## Bu Kurulumda Bilerek Basit Tuttugumuz Seyler

- kimlik dogrulama yok
- TLS yok
- persistence yok

Bu karar sadece lokal prova icindir. AWS asamasinda gercek servis ve guvenlik ayarlari farkli olacak.
