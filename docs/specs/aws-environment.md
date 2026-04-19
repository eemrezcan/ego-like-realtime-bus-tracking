# AWS Environment and Deployment Notes

Bu belge, projenin AWS tarafinda hangi erisim modeli ile calistirildigini, hangi kaynaklarin hangi bolgede olusturuldugunu ve final rapora alinabilecek teknik ozetleri kayit altina alir.

## AWS Erisim Modeli

Bu projede klasik `IAM user + access key` yaklasimi yerine `AWS IAM Identity Center (SSO)` kullanilmistir.

Bu secimin nedeni:

- kullanicinin AWS Console'a `Federated user` olarak giriyor olmasi
- root hesap veya kalici access key kullanmaktan kacinmak istememiz
- proje gelistirme akisinin daha guvenli ve modern bir AWS erisim modeli uzerinden ilerlemesi

SSO profili su sekilde olusturulmustur:

- CLI profile name: `eemrezcan`
- Account ID: `775755739642`
- Permission set / role: `AdministratorAccess`
- SSO region: `us-east-1`
- Default client region: `eu-central-1`
- Output format: `json`

## Neden SSO Kullanildi

Kullanicinin AWS konsolundaki gorunur kimligi `Federated user` oldugu icin `aws configure` ile sabit access key tanimlamak dogru yol degildi. Bunun yerine `aws configure sso` kullanildi.

Bu, final raporda su sekilde aciklanabilir:

`Projede AWS kimlik dogrulamasi icin IAM Identity Center (SSO) kullanilmistir. Bu sayede kalici access key yerine gecici ve yonetilebilir oturum bilgileriyle AWS servislerine erisim saglanmistir.`

## Kimlik Dogrulama Sonucu

SSO login sonrasi dogrulama basariyla yapilmistir. CLI tarafinda gorulen kimlik ozeti:

- Account: `775755739642`
- ARN: `arn:aws:sts::775755739642:assumed-role/AWSReservedSSO_AdministratorAccess_69166248b0fb415a/eemrezcan`

Bu bilgi, AWS kaynaklarinin kullanicinin bekledigi hesap uzerinde olusturuldugunu dogrulamak icin kullanilmistir.

## Kullandigimiz Bolgeler

Projede iki farkli AWS bolge kavrami vardir:

- `SSO region`: `us-east-1`
- `Resource region`: `eu-central-1`

Bu ayrim onemlidir:

- IAM Identity Center yapisi `us-east-1` tarafinda gorunur olabilir
- ancak proje kaynaklari `eu-central-1` bolgesinde olusturulmustur

Bu tercih, proje konfigurasyonundaki `AWS_REGION=eu-central-1` karari ile uyumludur.

## Olusturulan AWS Kaynaklari

### DynamoDB

Olusturulan tablolar:

- `bus_current_state`
- `telemetry_history`

Olusum amaci:

- `bus_current_state`: Her otobusun son durumunu saklamak
- `telemetry_history`: Gecmis telemetri kayitlarini saklamak

Olusum ozellikleri:

- billing mode: `PAY_PER_REQUEST`
- region: `eu-central-1`

Tablo durumlari:

- `bus_current_state`: `ACTIVE`
- `telemetry_history`: `ACTIVE`

### Kinesis Data Streams

Olusturulan stream:

- `ego-bus-telemetry-stream`

Olusum amaci:

- IoT Core'dan gelen telemetri verisini Lambda'ya tasiyacak gercek zamanli akis omurgasini kurmak

Stream durumu:

- `ACTIVE`

Region:

- `eu-central-1`

### IAM Role

Olusturulan Lambda execution role:

- `ego-bus-lambda-role`

Bu role icin baglanan inline policy, su servislere erisim verir:

- CloudWatch Logs
- Kinesis Data Streams
- DynamoDB

### Lambda

Olusturulan Lambda function:

- `ego-bus-processor`

Fonksiyon ozellikleri:

- runtime: `python3.12`
- handler: `processor.lambda_handler.lambda_handler`
- memory: `256 MB`
- timeout: `30 saniye`

Lambda ortam degiskenleri:

- `PROCESSOR_STORAGE_MODE=dynamodb`
- `DDB_CURRENT_STATE_TABLE=bus_current_state`
- `DDB_HISTORY_TABLE=telemetry_history`

Bu function, Kinesis'ten gelen ham telemetri event'lerini alir, ETA ve doluluk gibi turetilmis alanlari hesaplar ve sonucu DynamoDB'ye yazar.

### Event Source Mapping

Kinesis ile Lambda arasinda olusturulan event source mapping:

- source stream: `ego-bus-telemetry-stream`
- target function: `ego-bus-processor`
- status: `Enabled`
- last processing result: `OK`

Bu baglanti sayesinde stream'e dusen kayitlar otomatik olarak Lambda tarafinda islenmektedir.

### AWS IoT Core

Olusturulan IoT kaynaklari:

- IoT rule role: `ego-bus-iot-rule-role`
- IoT topic rule: `ego_bus_telemetry_to_kinesis`
- simulator thing: `ego-bus-simulator-device`
- simulator policy: `ego-bus-simulator-policy`

IoT Core data endpoint:

- `a17fmdwf2mfy6c-ats.iot.eu-central-1.amazonaws.com`

Topic rule SQL:

- `SELECT * FROM 'ego-sim/v1/bus/telemetry'`

Bu kuralin amaci, MQTT topic'ine gelen telemetri verisini `ego-bus-telemetry-stream` uzerine aktarmaktir.

Simulator cihazi icin bir istemci sertifikasi, private key ve public key olusturulmus; bu dosyalar yerel gelistirme ortaminda `build/aws/iot/device/` altina kaydedilmistir.

## Neden Once Bu Kaynaklar Kuruldu

AWS tarafina geciste su strateji izlendi:

1. Once kimlik dogrulama dogrulandi
2. Sonra veri omurgasi olan `DynamoDB` ve `Kinesis` kuruldu
3. Daha sonra Lambda ve IoT Core tarafina gecilecek

Bu siranin nedeni, hata ayiklamayi kolaylastirmaktir. Eger IoT Core en basta kurulsa ve veri akmasa, problemin MQTT, IAM, Lambda veya veritabani tarafinda oldugu belirsiz kalirdi. Bu nedenle once veri yazma ve akis kaynaklari ayaga kaldirildi.

## AWS Uzerinde Yapilan Dogrulamalar

Kurulum sonrasinda iki seviyede dogrulama yapilmistir:

### 1. Dogrudan Lambda Invoke

Gecerli bir ornek payload ile `ego-bus-processor` dogrudan invoke edilmis ve Lambda'nin kendi basina calistigi gorulmustur. Bu dogrulama sonrasi `bus_current_state` tablosunda `BUS_520_01` icin kayit olusmustur.

### 2. Kinesis Uzerinden Uctan Uca Test

Gecerli bir ornek telemetri kaydi `ego-bus-telemetry-stream` uzerine yazilmis ve sonrasinda `bus_current_state` tablosunda `BUS_520_03` icin beklenen veri gorulmustur.

Bu test, asagidaki zincirin calistigini gostermektedir:

`Kinesis -> Lambda -> DynamoDB`

### 3. AWS IoT Core Uzerinden Uctan Uca Test

AWS CLI ile IoT data endpoint'ine gecerli bir telemetri payload'i publish edilmis ve sonrasinda `bus_current_state` tablosunda `BUS_520_04` icin beklenen veri gorulmustur.

Bu test, asagidaki zincirin calistigini gostermektedir:

`IoT Core -> Kinesis -> Lambda -> DynamoDB`

### 4. Gercek Simulator Ile MQTT/TLS Testi

Simulator, olusturulan device sertifikasi, private key ve `AmazonRootCA1.pem` kullanilarak `8883` portu uzerinden AWS IoT Core'a baglanmistir.

Ilk denemede uzak broker icin publish guvenilirligi dusuk kalmis, sonrasinda MQTT publish tarafinda `QoS 1` ve `wait_for_publish()` kullanilarak iletim garanti altina alinmistir.

Bu iyilestirme sonrasi `bus_current_state` tablosunda `BUS_510_01` icin simulator tarafindan uretilmis veri gorulmustur.

Bu, hedeflenen mimarinin asagidaki zincirle gerceklestigini gostermektedir:

`Simulator -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB`

### 5. FastAPI Uzerinden DynamoDB Okuma Testi

API katmani `dynamodb` modunda, `AWS_PROFILE=eemrezcan` ve `AWS_REGION=eu-central-1` ayarlari ile calistirilmistir.

Yerel dogrulamada `uvicorn` kisa sureli olarak ayaga kaldirilmis ve asagidaki endpoint'ler basariyla cevap donmustur:

- `/health`
- `/summary`
- `/buses`

Bu testte API, `bus_current_state` tablosundaki gercek AWS verisini okuyabilmistir. Ornek olarak `BUS_510_01`, `BUS_510_02` ve `BUS_510_03` kayitlari line name ve turetilmis alanlarla birlikte endpoint cevabinda gorulmustur.

Bu dogrulama, asagidaki zincirin de hazir oldugunu gostermektedir:

`DynamoDB -> FastAPI`

### 6. Dashboard Uzerinden AWS Verisi Gostermi

FastAPI uygulamasi `dynamodb` modunda `bus_current_state` tablosuna bagli olarak ayaga kaldirilmistir. Ardindan Streamlit dashboard `DASHBOARD_API_BASE_URL` uzerinden bu API'ye baglanmis ve sorunsuz acilmistir.

Dogrulanan noktalar:

- API health cevabi `storage_mode=dynamodb` donmustur
- API summary cevabi gercek AWS verisiyle gelmistir
- Streamlit dashboard HTTP `200` ile cevap vermistir

Bu adim, asagidaki tam zincirin goruntuleme katmanina kadar hazir oldugunu gostermektedir:

`Simulator -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

## Karsilasilan Teknik Notlar

- Ilk Lambda deploy denemesinde `AWS_REGION` ortam degiskenini elle set etmeye calismak hata vermistir. Bu alan Lambda tarafinda rezerve oldugu icin script'ten cikarilmistir.
- Ilk paketlemede `simulator/` klasoru zip icine alinmadigi icin `No module named 'simulator'` hatasi alinmistir. Paketleme script'i buna gore guncellenmistir.
- Ilk Kinesis denemelerinde gecersiz `bus_id` degerleri kullanildigi icin batch hata ile dusmustur. Sonrasinda `lambda_handler` kayit bazli toleransli hale getirilmis ve gecersiz payload'lar loglanip diger kayitlarin islenmesi saglanmistir.
- IoT Core uzerinden gercek simulator publish testinde uzak broker'a cikis yapan istemci cok hizli kapanabildigi icin MQTT publish katmaninda `QoS 1` ve `wait_for_publish()` kullanilmistir.

## Repo Tarafindaki AWS Dosyalari

Bu kurulumlari tekrar edilebilir hale getirmek icin repoda su dosyalar tutulur:

- `infra/aws/cli/create-dynamodb-tables.ps1`
- `infra/aws/cli/create-kinesis-stream.ps1`
- `infra/aws/cli/package-lambda.ps1`
- `infra/aws/cli/create-lambda-role.ps1`
- `infra/aws/cli/create-or-update-lambda.ps1`
- `infra/aws/cli/create-event-source-mapping.ps1`
- `infra/aws/cli/create-iot-rule-role.ps1`
- `infra/aws/cli/create-or-update-topic-rule.ps1`
- `infra/aws/cli/create-iot-simulator-device.ps1`
- `infra/aws/cli/download-amazon-root-ca.ps1`
- `infra/aws/iam/lambda-trust-policy.json`
- `infra/aws/iam/lambda-inline-policy.json`
- `infra/aws/iam/iot-rule-trust-policy.json`
- `infra/aws/iot/telemetry-topic-rule.sql`
- `infra/aws/iot/simulator-device-policy.json`
- `docs/planning/aws-rollout-plan.md`

Bu dosyalar final raporda "kurulum tekrar edilebilirligi" ve "mimari disiplin" acisindan faydali referanslar sunar.

## Final Rapora Koyulabilecek Ozet Metin

`AWS tarafinda kimlik dogrulama icin IAM Identity Center (SSO) kullanilmistir. Kaynaklar eu-central-1 bolgesinde olusturulmus; iki adet DynamoDB tablosu (bus_current_state, telemetry_history), bir adet Kinesis Data Stream (ego-bus-telemetry-stream), bir adet Lambda function (ego-bus-processor), buna bagli IAM execution role, bir adet IoT topic rule ve simulator cihaz sertifikasi aktif hale getirilmistir. Kinesis ile Lambda arasinda event source mapping kurularak verinin otomatik islenmesi saglanmis; hem AWS CLI ile IoT Core uzerinden, hem de dogrudan simulator uygulamasi ile MQTT/TLS uzerinden gonderilen ornek telemetri kayitlarinin bulutta islenip DynamoDB'ye yazildigi dogrulanmistir. Son olarak FastAPI katmaninin `dynamodb` modunda bu verileri okuyabildigi ve Streamlit dashboard'un ayni API uzerinden gercek AWS verisini gosterebildigi kanitlanmistir.`
