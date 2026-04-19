# Final Report Preview

Bu dosya, `report/` altindaki LaTeX raporunun duz metin onizleme surumudur.

Buradan rahat okuyabilirsin:

- [main.tex](./main.tex) ana rapor yapisi
- [references.bib](./references.bib) kaynakca
- [sections](./sections) teknik bolumler

## Baslik

EGO-Benzeri Sentetik Veri ile Gercek Zamanli Otobus Takip ve Yogunluk Analiz Sistemi

## Ozet

Bu calismada, sentetik veri ureten bir toplu tasima telemetri sistemi gelistirilmis ve bu verinin MQTT tabanli bir akis ile AWS uzerinde gercek zamanli olarak islenmesi saglanmistir. Projede otobusler, belirli araliklarla konum, hiz, hat bilgisi ve kart basimina dayali binis sayisi ureten sanal cihazlar olarak modellenmistir. Uretilen telemetri verileri AWS IoT Core uzerinden sisteme alinmis, IoT kurali araciligiyla Amazon Kinesis Data Streams katmanina aktarilmis ve AWS Lambda fonksiyonu ile zenginlestirilerek Amazon DynamoDB tablolarina yazilmistir. Islenen veriler FastAPI tabanli bir okuma katmani ile sunulmus ve Streamlit tabanli bir dashboard uzerinden canli olarak gorsellestirilmistir.

Calismada ham veri ile turetilmis veri acik bicimde ayrilmistir. Konum, hiz ve binis sayisi simulator tarafinda uretilirken; tahmini varis suresi, tahmini inis miktari, doluluk seviyesi ve gecikme bilgisi bulut tarafinda hesaplanmistir. Bu yaklasim, projeyi yalnizca gorsel bir simulasyon olmaktan cikarmis ve gercek zamanli veri isleme mimarisinin uctan uca hayata gecirildigi bir uygulamaya donusturmustur. Elde edilen sonuc, AWS servisleri kullanilarak kurulan MQTT tabanli veri hatti ile sentetik otobus telemetrisinin basarili bicimde islenebildigini, depolanabildigini ve canli izleme amacli bir arayuze aktarilabildigini gostermistir.

## Anahtar Kelimeler

- MQTT
- AWS IoT Core
- Kinesis Data Streams
- AWS Lambda
- DynamoDB
- FastAPI
- Streamlit
- real-time bus tracking

## Icindekiler

1. Giris
2. Problem Tanimi ve Kapsam
3. Sistem Mimarisi
4. Veri Modeli ve Olay Semasi
5. Gercekleme Ayrintilari
6. AWS Dagitimi ve Gercek Ortam Dogrulamasi
7. Sonuclar ve Degerlendirme
8. Sonuc
9. Kaynakca

## Giris

Gercek zamanli konum ve durum izleme sistemleri, modern toplu tasima altyapilarinin en gorunur bilesenlerinden biridir. Yolcularin otobusun mevcut konumunu, tahmini varis suresini ve hatta yogunluk seviyesini takip edebilmesi, hizmet kalitesini dogrudan etkileyen bir unsurdur. Benzer sekilde, isletmeci kurumlar acisindan da canli telemetri verisi; hat optimizasyonu, gecikme tespiti ve operasyonel izleme icin yuksek deger tasir. Bu nedenle toplu tasimada gercek zamanli veri akisi, yalnizca bir bilgi ekrani problemi degil, ayni zamanda bulut tabanli veri isleme ve servis butunlestirme problemidir.

Bu projede, gercek EGO verisi veya fiziksel cihazlar kullanilmadan, EGO-benzeri bir otobus takip sistemi sentetik veri ile modellenmistir. Buradaki temel amac, gercek bir kurum verisine bagli kalmadan, otobus telemetrisinin MQTT tabanli bir yapi ile buluta aktarilmasi, bulutta islenmesi ve bir dashboard uzerinden canli olarak izlenmesi surecini gostermektir. Bu tercih, dersin odak noktasini veri kaynagindan cok mimari tasarim, servis entegrasyonu ve gercek zamanli akis yonetimi uzerine tasimaktadir. Ayrica sentetik veri kullanimi, sistem tasarimini test etmeyi kolaylastirirken gercek kurum verisine bagimlilik gibi operasyonel kisitlari da ortadan kaldirmaktadir.

Calismanin ana katkisi, veri uretimi, bulut uzerinde zenginlestirme ve canli sunum katmanlarini tek bir yapi altinda birlestirmesidir. Simulator tarafinda yalnizca ham telemetri verisi uretilmis; ETA, tahmini inis miktari, doluluk ve gecikme gibi karar verici bilgiler ise AWS uzerinde hesaplanmistir. Boylece sistem, sadece sabit veri gosteren bir demo olmaktan cikmis, gercek zamanli olay akisina dayali bulut tabanli bir referans mimariye donusmustur.

## Problem Tanimi ve Kapsam

Bu proje, EGO benzeri bir toplu tasima takip sisteminin teknik cekirdeginin sentetik veri ile modellenmesini hedeflemektedir. Temel problem, hareket halindeki otobuslerden gelen telemetri verisinin gercek zamanli olarak toplanmasi, bulut uzerinde islenmesi, operasyonel olarak anlamli hale getirilmesi ve son kullaniciya anlik olarak sunulmasidir. Bu tanim, calismanin odagini basit bir harita gosteriminden ayirmakta; veri akisi, bulut servis entegrasyonu ve olay tabanli isleme mantigini merkeze almaktadir.

Projede ham veri ile turetilen veri birbirinden acik bicimde ayrilmistir. Ham veri, simulator tarafinda uretilen `bus_id`, `line_id`, `lat`, `lon`, `speed_kmh`, `next_stop_id`, `next_stop_name`, `boarding_count` ve `timestamp` alanlarindan olusmaktadir. Buna karsilik `estimated_eta_sec`, `estimated_alighting_count`, `estimated_occupancy_score`, `estimated_occupancy_level` ve `is_delayed` alanlari bulut tarafinda hesaplanmistir. Bu ayrim, sistemin yalnizca veri gosteren bir simulasyon olmadigini, veriyi yorumlayan ve zenginlestiren bir bulut isleme katmani kurdugunu gostermektedir.

Calisma kapsaminda sistem, MVP mantigiyla sinirlandirilmis ve uc hat, hat basina birden fazla otobus ve tanimli durak/rota dizileri uzerinden ilerleyecek sekilde modellenmistir. Gercek EGO altyapisina baglanti kurulmamistir; fiziksel otobus cihazlari, GPS modulleri veya kart okuyucular kullanilmamistir. Makine ogrenmesi tabanli tahminleme, kullanici girisi, mobil istemci, dinamik rota optimizasyonu ve gercek trafik verisi entegrasyonu gibi genisletilebilir bilesenler bu asamada bilerek kapsam disinda birakilmistir. Boylece proje kapsami, ders gereksinimlerine uygun olarak gercek zamanli veri akisi, bulut isleme, depolama ve gorsellestirme ekseninde kontrollu bicimde tutulmustur.

Bu kapsam siniri, raporun degerlendirme mantigi acisindan da onemlidir. Basari olcutu, gercek bir belediye sisteminin tum karmasikligini taklit etmek degil; secilen mimarinin veri uretimi, MQTT tabanli iletim, AWS uzerinde zenginlestirme, DynamoDB ile depolama ve dashboard ile canli izleme asamalarini uctan uca yerine getirebilmesidir.

## Sistem Mimarisi

Genel veri akisi su sekildedir:

`Bus Simulator -> MQTT -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit`

Bu mimaride simulator katmani, otobusleri sanal veri ureticileri olarak modellemektedir. Her otobus belirli bir hatta, yon bilgisine ve rota segmentine bagli olarak konum guncellemekte; ardindan bu veri MQTT topic'i uzerinden yayimlanmaktadir. MQTT'nin publish/subscribe yapisi, dusuk ek yuk ve cihaz-bulut haberlesmesine uygunlugu nedeniyle tercih edilmistir. Bu secim, otobuslerin birer IoT cihazi gibi davranmasini saglayarak proje senaryosunu daha inandirici hale getirmektedir.

AWS IoT Core, MQTT istemcilerinden gelen mesajlari guvenli bicimde kabul eden yonetilen giris noktasi olarak kullanilmistir. IoT Core'a gelen mesajlar, bir IoT kurali yardimiyla Amazon Kinesis Data Streams'e yonlendirilmektedir. Kinesis burada telemetri verisini surekli ve dusuk gecikmeli sekilde kabul eden akis omurgasi olarak gorev yapmaktadir. Bu secim sayesinde veri girisi ile isleme katmani birbirinden ayrilmistir.

AWS Lambda, Kinesis uzerinden gelen olaylari okuyup ETA, tahmini inis, doluluk ve gecikme bilgisini hesaplamaktadir. Yani sistemin karar ureten kismi bulut tarafinda konumlanmaktadir. Islenen veriler daha sonra biri anlik durum, digeri ise telemetri gecmisi icin kullanilan iki farkli DynamoDB tablosuna yazilmaktadir.

FastAPI veri sunum katmanini, Streamlit ise son kullanici arayuzunu saglamaktadir. Bu yapi sayesinde veri kaynagi ile arayuz arasina net bir API katmani konmus, mimari hem daha moduler hem de daha savunulabilir hale getirilmistir.

Buraya daha sonra su gorseller eklenecek:

- BURAYA SISTEM MIMARISI DIYAGRAMI GELECEK

## Veri Modeli ve Olay Semasi

Sistem veri modeli uc ana bilesenden olusmaktadir: hatlar, duraklar ve rotalar. `data/` klasoru altinda tanimlanan JSON dosyalari, simulatorun hangi otobusun hangi hat uzerinde hareket edecegini, hangi duraklara yaklasacagini ve ETA hesaplamasinda hangi segment bilgilerini kullanacagini belirlemektedir. Bu yapi, simulator ile bulut isleme katmani arasinda ortak bir referans modeli olusturmaktadir. Baska bir ifadeyle veri modeli, yalnizca test verisi tutan statik bir klasor degil; hem simulatorun hareket mantigini hem de bulut tarafindaki hesaplama baglamini belirleyen cekirdek tasarim katmanidir.

Ham olay semasi, MQTT uzerinden gonderilen telemetri paketinin catisini tanimlamaktadir. Olay semasinin ayri bir JSON Schema dosyasi ile tanimlanmasi, simulator, Lambda ve API katmanlari arasindaki veri sozlesmesini sabitlemistir. Boylece bir katmanda yapilan degisiklik diger katmanlar icin belirsizlik uretmemektedir.

Ham olay alanlari:

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

Bulutta uretilen alanlar:

- `estimated_eta_sec`
- `estimated_alighting_count`
- `estimated_occupancy_score`
- `estimated_occupancy_level`
- `is_delayed`

Bu projedeki kritik tasarim karari, olculen veri ile tahmin edilen verinin ayrilmasidir. Binis sayisi simulator tarafinda dogrudan uretilirken, inis miktari bulutta tahmin edilmekte ve o ana kadarki doluluk skoru ile birlikte yeniden hesaplanmaktadir. ETA de yine konum, hiz ve durak mesafesi bilgisi uzerinden Lambda tarafinda uretilmektedir. Bu tercih, sistemin basit bir sahte veri gosteriminden cikarak gercek zamanli veri zenginlestirme mimarisine donusmesini saglamistir. Ayni zamanda hangi bilginin gozlemlendigi hangi bilginin tahmin edildigi acik bicimde ayristirildigi icin raporun teknik durustlugunu da guclendirmektedir.

## Gercekleme Ayrintilari

Simulator katmani Python ile gelistirilmis bir olay uretim aracidir. Bu katman, veri modelinde tanimlanan hat, durak ve rota bilgilerini okuyarak her hat icin birden fazla otobus nesnesi uretmektedir. Her iterasyonda otobuslerin segment uzerindeki konumu guncellenmekte, hizlari yeniden hesaplanmakta ve duraga bagli olarak binis sayisi uretilmektedir. Olusan payload, stdout, dosya veya MQTT modlari ile yayinlanabilmektedir. Projenin son asamasinda simulatora `--continuous` secenegi eklenmis ve boylece dashboard tarafinda surekli veri akisi gozlenebilir hale gelmistir. AWS dogrulama asamasinda MQTT/TLS modu kullanilmis ve simulator AWS IoT Core endpoint'ine istemci sertifikasi ile baglanmistir.

Bulut isleme mantigi AWS Lambda uzerinde calisan Python kodu ile uygulanmistir. Lambda, Kinesis uzerinden gelen telemetri paketlerini alip once dogrulamakta, daha sonra ETA, tahmini inis, doluluk skoru ve gecikme bilgisini hesaplamaktadir. ETA hesabi, mevcut konum, hiz ve siradaki duraga ait segment bilgisi kullanilarak uretilmektedir. Tahmini inis miktari ise mevcut doluluk ve durak baglamina dayali kural tabanli bir yaklasimla elde edilmektedir. Batch isleme mantiginda hata toleransi eklenmis; boylece gecersiz bir kayit geldigi durumda tum batch yerine yalnizca hatali kayit atlanmistir. Bu karar, akis hattinin daha dayanikli calismasini saglamistir. Isleme kurallarinin ana hedefi, ham veriyi olabildigince az varsayimla anlamli operasyonel bilgiye donusturmektir.

DynamoDB tarafinda iki tablo kullanilmistir:

- `bus_current_state`
- `telemetry_history`

Bu iki tabloya ayrilmis tasarim, operasyonel izleme ile tarihsel kayit ihtiyacini birbirinden ayirmakta ve sistemin hem canli arayuz hem de raporlama acisindan daha kullanisli olmasini saglamaktadir.

FastAPI tarafinda temel endpoint'ler:

- `/health`
- `/summary`
- `/buses`
- `/buses/{id}`
- `/lines`

Bu yapi sayesinde veri sunumu katmani ile depolama katmani birbirinden ayrilmis, ayrica yerel dosya modu ile DynamoDB modu arasinda gecis de kolaylastirilmistir. Boylece ayni dashboard hem lokal dogrulama asamasinda hem de AWS destekli gercek ortamda tekrar kullanilabilmistir.

Dashboard tarafinda sistem durumu banner'i, ozet metrik kartlari, hat bazli kartlar, otobus tablosu ve pydeck tabanli canli harita bulunmaktadir. Son asamada harita gorunurlugu artirilmis, otomatik yenileme davranisi eklenmis ve veri tazeligi gostergesi olusturulmustur. Bu tasarim karari, hem test edilebilirligi hem de demo sirasinda veri akisinin daha anlasilir sunulmasini kolaylastirmistir.

## AWS Dagitimi ve Gercek Ortam Dogrulamasi

AWS tarafinda erisim yonetimi icin IAM Identity Center tabanli SSO yapisi kullanilmistir. Kaynaklar `eu-central-1` bolgesinde olusturulurken, SSO yapisinin `us-east-1` tarafinda tanimli oldugu not edilmistir. Bu ayrim, dagitim surecinin ilk adimlarinda karsilasilan temel operasyonel noktalardan biri olmustur.

Olusturulan temel kaynaklar:

- `bus_current_state`
- `telemetry_history`
- `ego-bus-telemetry-stream`
- `ego-bus-lambda-role`
- `ego-bus-processor`
- `ego-bus-iot-rule-role`
- `ego_bus_telemetry_to_kinesis`
- `ego-bus-simulator-device`

Dogrulama asama asama yapilmistir:

1. Lambda dogrudan invoke edilerek test edildi
2. Kinesis uzerinden veri akisi kontrol edildi
3. AWS CLI ile IoT publish testi yapildi
4. Python simulatoru MQTT/TLS ile AWS IoT Core'a baglandi
5. FastAPI ve Streamlit katmaninda son kullanici gorunumu dogrulandi

Bu zincir, projenin yalnizca lokal ortamda degil, AWS uzerinde de uctan uca calistigini gostermektedir. Dogrulama surecinde yalnizca servislerin olusmasi degil, gercek veri gecisinin izlenmesi esas alinmistir. Son asamada FastAPI uzerinden okunan `latest_timestamp` bilgisinin degismesi ve Streamlit dashboard'da otobus konumlarinin yenilenmesi, zincirin son kullanici tarafinda da tamamlandigini gostermistir.

Buraya daha sonra su gorseller eklenecek:

- BURAYA AWS KAYNAKLARI VE DOGRULAMA EKRAN GORUNTUSU GELECEK

## Sonuclar ve Degerlendirme

Sistemin temel hedefi yerine getirilmistir. Sentetik otobus telemetrisi MQTT ile buluta aktarilmis, AWS uzerinde islenmis, veritabaninda saklanmis ve canli dashboard uzerinde goruntulenmistir. Yerel ve AWS destekli dogrulama adimlarinda simulator, processor, API ve dashboard katmanlarinin birlikte calistigi gorulmustur. Ozellikle `Simulator -> AWS IoT Core -> Kinesis -> Lambda -> DynamoDB -> FastAPI -> Streamlit` zincirinin gercek veri ile dogrulanmasi, calismanin teknik gucunu artiran en onemli sonuc olmustur.

Dogrulanan temel kazanımlar:

- MQTT tabanli sentetik telemetri akisi kuruldu
- AWS IoT Core uzerinden gelen veri Kinesis'e aktarildi
- Lambda ile zenginlestirme yapildi
- Ham veri ile turetilmis veri ayrimi korundu
- DynamoDB uzerinden anlik durum okunabildi
- Dashboard canli veri akisina tepki verebilir hale geldi

Buraya daha sonra su gorseller eklenecek:

- BURAYA DASHBOARD EKRAN GORUNTUSU GELECEK

Projede karsilasilan temel zorluklar daha cok entegrasyon katmaninda ortaya cikmistir. AWS CLI kimlik dogrulama yontemi, IoT sertifika dosyalarinin dogru konumlandirilmasi, Lambda paketleme sureci, batch icinde hatali kayitlarin etkisinin sinirlandirilmasi ve Streamlit tarafindaki canli yenileme davranisi bu surecte cozulmesi gereken basliklar olmustur. Ancak bu zorluklar ayni zamanda sistemin raporlanabilirligini de guclendirmistir; cunku proje sadece teorik bir mimari olarak kalmamis, uygulama ve hata ayiklama asamalariyla birlikte gercek bir gelistirme surecine donusmustur.

Sistemin sinirlari da aciktir. Kullanilan veri tamamen sentetiktir; dolayisiyla gercek yolcu davranisi, trafik etkisi ve arac telemetrisi tam olarak modellenmemektedir. Yogunluk ve gecikme hesaplari kural tabanli olarak uretilmistir ve bu nedenle gercek dunyadaki karmasik davranisi tam olarak temsil etmemektedir. Buna ragmen dersin hedefleri acisindan sistem yeterli bir teknik derinlik sunmaktadir. Gelecek calismalarda makine ogrenmesi tabanli ETA tahmini, gercek trafik verisi entegrasyonu, daha gelismis yolcu yogunluk modeli ve mobil istemci arayuzu gibi genisletmeler ele alinabilir.

## Sonuc

Bu projede, EGO-benzeri bir otobus takip sisteminin sentetik veri ile modellenmesi ve bu verinin AWS tabanli gercek zamanli bir akis mimarisi uzerinde islenmesi basarili bicimde gerceklestirilmistir. Sistem; veri uretimi, cihaz-bulut haberlesmesi, akisa dayali isleme, depolama ve gorsellestirme katmanlarini butunlesik bir sekilde bir araya getirmektedir. Ham veri ile turetilmis veri arasindaki ayrimin korunmasi ve karar ureten alanlarin bulutta hesaplanmasi, calismanin teknik anlamini guclendirmistir.

Sonuc olarak, bu calisma bulut bilisim dersinin temel hedefleriyle uyumlu bir sekilde, MQTT tabanli gercek zamanli veri akisi ile AWS servis entegrasyonunu pratikte gosteren bir referans uygulama ortaya koymustur. Proje ayni zamanda, sentetik veri kullanilsa dahi dogru mimari kararlar, uygun servis secimi ve sistematik dogrulama adimlari ile akademik olarak savunulabilir, tekrar edilebilir ve gosterilebilir bir sistem kurulabilecegini gostermistir.

## Kaynakca

Kaynakca ana dosyasi:

- [references.bib](./references.bib)
