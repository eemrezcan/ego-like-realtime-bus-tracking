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

## Karsilasilan Teknik Notlar

- Ilk Lambda deploy denemesinde `AWS_REGION` ortam degiskenini elle set etmeye calismak hata vermistir. Bu alan Lambda tarafinda rezerve oldugu icin script'ten cikarilmistir.
- Ilk paketlemede `simulator/` klasoru zip icine alinmadigi icin `No module named 'simulator'` hatasi alinmistir. Paketleme script'i buna gore guncellenmistir.
- Ilk Kinesis denemelerinde gecersiz `bus_id` degerleri kullanildigi icin batch hata ile dusmustur. Sonrasinda `lambda_handler` kayit bazli toleransli hale getirilmis ve gecersiz payload'lar loglanip diger kayitlarin islenmesi saglanmistir.

## Repo Tarafindaki AWS Dosyalari

Bu kurulumlari tekrar edilebilir hale getirmek icin repoda su dosyalar tutulur:

- `infra/aws/cli/create-dynamodb-tables.ps1`
- `infra/aws/cli/create-kinesis-stream.ps1`
- `infra/aws/cli/package-lambda.ps1`
- `infra/aws/cli/create-lambda-role.ps1`
- `infra/aws/cli/create-or-update-lambda.ps1`
- `infra/aws/cli/create-event-source-mapping.ps1`
- `infra/aws/iam/lambda-trust-policy.json`
- `infra/aws/iam/lambda-inline-policy.json`
- `infra/aws/iot/telemetry-topic-rule.sql`
- `infra/aws/iot/simulator-device-policy.json`
- `docs/planning/aws-rollout-plan.md`

Bu dosyalar final raporda "kurulum tekrar edilebilirligi" ve "mimari disiplin" acisindan faydali referanslar sunar.

## Final Rapora Koyulabilecek Ozet Metin

`AWS tarafinda kimlik dogrulama icin IAM Identity Center (SSO) kullanilmistir. Kaynaklar eu-central-1 bolgesinde olusturulmus; iki adet DynamoDB tablosu (bus_current_state, telemetry_history), bir adet Kinesis Data Stream (ego-bus-telemetry-stream), bir adet Lambda function (ego-bus-processor) ve buna bagli IAM execution role aktif hale getirilmistir. Kinesis ile Lambda arasinda event source mapping kurularak verinin otomatik islenmesi saglanmis, ornek telemetri kayitlari uzerinden verinin bulutta islenip DynamoDB'ye yazildigi dogrulanmistir.`
