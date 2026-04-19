# Proje Dokumantasyonu

Bu klasor, proje boyunca alinacak kararlarin dagilmamasi ve gelistirme sirasinin net kalmasi icin tutulur.

## Okuma Sirasi

Projeye yeniden baslarken veya yeni bir karar alirken dosyalari su sirayla okumak gerekir:

1. `planning/implementation-roadmap.md`
2. `decisions/001-proje-vizyonu.md`
3. `decisions/002-mvp-kapsami.md`
4. `decisions/003-teknik-yigin.md`
5. `specs/data-model.md`
6. `specs/data-contract.md`
7. `specs/event-schema.md`
8. `specs/dependencies.md`
9. `specs/architecture.md`
10. `planning/local-broker-setup.md`
11. `specs/dynamodb-design.md`
12. `specs/api-design.md`
13. `specs/dashboard-design.md`
14. `planning/aws-rollout-plan.md`
15. `specs/aws-environment.md`
16. `planning/report-roadmap.md`
17. `specs/report-sources.md`
18. `worklogs/05.04.2026.md`
19. `worklogs/19.04.2026.md`

## Ilk Baslangic Noktasi

Bu proje icin ilk dondurulmasi gereken konu teknoloji secimi degil, veri sozlesmesidir.

Netlestirilmesi gereken ilk ilke:

`Otobus simulatoru sadece ham telemetri ve kart basim sayisi uretir; ETA, tahmini inis, doluluk ve gecikme bulutta hesaplanir.`

Bu ilke dondurulmadan kod yazimina gecilmemelidir.

## Klasor Yapisi

- `decisions/`: Dondurulmus kararlar ve gerekceleri
- `specs/`: Sistemin teknik tarifi, veri yapilari ve mimari akisi
- `planning/`: Nereden baslanacagi, sira ve uygulama plani
- `worklogs/`: Gunluk ilerleme kayitlari ve oturum ozetleri

Ek olarak:

- `schemas/`: Makine tarafindan okunabilir resmi veri semalari

## Su Ana Kadarki Cekirdek Kararlar

- Proje adi: `EGO-benzeri sentetik veri ile gercek zamanli otobus takip ve yogunluk analiz sistemi`
- Protokol: `MQTT`
- Bulut platformu: `AWS`
- Giris noktasi: `AWS IoT Core`
- Isleme hatti: `AWS IoT Core Rule -> Kinesis Data Streams -> Lambda`
- Veritabani: `DynamoDB`
- Backend: `Python + FastAPI`
- Dashboard: `Streamlit`

## Dokumantasyon Kuralimiz

Yeni teknik karar alindiginda once ilgili dokumana eklenir, sonra kod degisimi yapilir.
