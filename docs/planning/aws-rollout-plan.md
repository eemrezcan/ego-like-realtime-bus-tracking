# AWS Rollout Plan

Bu belge yerelde calisan MVP'yi AWS uzerine tasirken hangi sirayla ilerleyecegimizi dondurur. Amaç, konsolda rastgele servis olusturmak yerine kontrollu bir dagitim akisi izlemektir.

## Hedef Akis

`Simulator -> AWS IoT Core -> IoT Rule -> Kinesis Data Streams -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

## Asama 1: Temel AWS Kaynaklari

Ilk kurulacak kaynaklar:

- `bus_current_state` DynamoDB tablosu
- `telemetry_history` DynamoDB tablosu
- bir adet `Kinesis Data Stream`
- Lambda execution role

Bu asamanin amaci, veri yazma ve akitma omurgasini hazir etmektir.

## Asama 2: Lambda Paketleme ve Dagitim

Processor kodu AWS Lambda olarak paketlenecek. Su nokta kritik:

- `processor/` klasoru zip icine alinacak
- `data/` klasoru de Lambda paketinde bulunacak
- Lambda handler: `processor.lambda_handler.lambda_handler`

Bu repo icindeki config dosyalari `python-dotenv` olmasa da calisacak sekilde guncellendi. Boylece Lambda'ya ek bagimlilik yukleme zorunlulugu azaltilmis oldu.

## Asama 3: IoT Core Giris Katmani

Kurulacak bilesenler:

- bir adet IoT policy
- simulator icin device certificate
- MQTT topic kabul edecek IoT rule

Kullandigimiz topic:

`ego-sim/v1/bus/telemetry`

IoT rule bu topic'ten gelen payload'i Kinesis stream'ine aktaracak.

## Asama 4: Event Source Mapping

Kinesis stream ile Lambda arasinda event source mapping olusturulacak. Boylece Lambda, stream icindeki record'lari toplu halde alip `processor.lambda_handler` icinden isleyecek.

Bu repo tarafinda Kinesis event envelope destegi zaten bulunuyor.

## Asama 5: Runtime Konfigurasyonu

Lambda icin gerekli environment variable'lar:

- `PROCESSOR_STORAGE_MODE=dynamodb`
- `AWS_REGION=<region>`
- `DDB_CURRENT_STATE_TABLE=bus_current_state`
- `DDB_HISTORY_TABLE=telemetry_history`

API icin gerekli environment variable'lar:

- `API_STORAGE_MODE=dynamodb`
- `AWS_REGION=<region>`
- `DDB_CURRENT_STATE_TABLE=bus_current_state`

## Asama 6: Uctan Uca Dogrulama

Kurulum bittiginde su adimlarla dogrulama yapilacak:

1. Simulator AWS IoT Core endpoint'ine TLS ile baglanir.
2. IoT Core mesaji Kinesis'e aktarir.
3. Lambda record'u isler ve DynamoDB'ye yazar.
4. FastAPI `dynamodb` modunda bu veriyi okur.
5. Streamlit dashboard canli veriyi gosterir.

## Bu Asamada Bilerek Yapmadiklarimiz

- Terraform veya CloudFormation ile tam otomatik dagitim
- API ve dashboard'u AWS uzerine deploy etme
- CloudWatch dashboard ve alarm yapilari

Bu MVP icin oncelik, veri akisinin AWS tarafinda gercekten calistigini gostermektir.
