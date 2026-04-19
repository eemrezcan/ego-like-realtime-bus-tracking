# AWS Infra

Bu klasor, AWS uzerine gecis icin gereken yardimci scriptleri, policy taslaklarini ve kurulum notlarini tutar.

## Klasorler

- `cli/`: AWS CLI ile calistirilacak PowerShell yardimci scriptleri
- `iam/`: Role trust policy ve inline policy taslaklari
- `iot/`: IoT topic ve policy taslaklari

## Ilk Hedef

Bu klasordeki dosyalarla sunlari kontrollu sekilde kurmak:

- DynamoDB tabloları
- Kinesis stream
- Lambda role ve policy
- Lambda paketleme ve deploy
- Kinesis -> Lambda event source mapping
- IoT rule role ve simulator device policy
- IoT topic rule ve simulator certificate
- IoT Core TLS baglantisi icin root CA indirme
- IoT topic rule

## Not

Bu klasor simdilik tam otomatik dagitim degil, tekrar edilebilir kurulum iskeleti icin tutulur.
