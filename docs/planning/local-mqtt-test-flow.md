# Lokal MQTT Test Akisi

Bu belge "lokal MQTT akisini netlestirmek" ifadesinin ne anlama geldigini anlatir.

## Amac

AWS tarafina gecmeden once simulatorun gercekten MQTT mantigiyla veri urettigini ve disaridan izlenebildigini gormek.

Bu asama sunlari kanitlar:

- topic dogru mu
- payload yapisi dogru mu
- eventler belli araliklarla akiyor mu
- bir MQTT istemcisi bu eventleri tuketebiliyor mu

## Akis

Lokal testte hedef akisimizi su sekilde kurariz:

`Bus Simulator -> Lokal MQTT Broker -> MQTT Inspector`

## Bilesenler

### Simulator

`python -m simulator` ile calisan event ureticidir.

### Lokal MQTT Broker

Yerelde kosan bir broker gerekir. Ornek olarak Mosquitto kullanilabilir.

Bu repoda broker kurulumu iki yol ile dusunuldu:

- Docker Compose ile Mosquitto
- Python tabanli fallback broker (`simulator.local_broker`)

Detay:

- `docs/planning/local-broker-setup.md`

### MQTT Inspector

Subscriber gibi davranir ve gelen mesajlari terminale basar.

Bu repo icinde:

- `simulator/mqtt_inspector.py`

## Deneme Sirasi

1. Lokal MQTT broker ayaga kaldirilir
2. Inspector aboneligi baslatilir
3. Simulator MQTT output ile calistirilir
4. Inspector tarafinda eventlerin aktigi gorulur

## Ornek Komutlar

Broker, Docker ile:

```powershell
docker compose -f docker-compose.local.yml up --build -d
```

Broker, Docker yoksa Python fallback ile:

```powershell
.\.venv\Scripts\python.exe -m simulator.local_broker --host 127.0.0.1 --port 1883
```

Inspector:

```powershell
.\.venv\Scripts\python.exe -m simulator.mqtt_inspector --broker-host localhost --broker-port 1883
```

Simulator:

```powershell
.\.venv\Scripts\python.exe -m simulator --steps 5 --interval-seconds 3 --output mqtt --broker-host localhost --broker-port 1883 --no-sleep
```

## Basarili Sonuc Nasil Gorunur

Basarili durumda inspector ekraninda su seyler gorulur:

- dogru topic
- parse edilebilen JSON payload
- her otobus icin tekrar eden eventler
- alan adlari schema ile uyumlu veri

## Bu Asama Neyi Cozmez

Bu test henuz sunlari kanitlamaz:

- AWS IoT Core entegrasyonu
- Kinesis akisi
- Lambda isleme mantigi
- DynamoDB yazimi

Yani bu adim sadece "yerel veri akisinin ve event formatinin saglamligi" icin vardir.
