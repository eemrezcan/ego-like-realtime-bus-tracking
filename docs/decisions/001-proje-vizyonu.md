# Karar 001: Proje Vizyonu

## Karar

Proje, `EGO-benzeri sentetik veri ile gercek zamanli otobus takip ve yogunluk analiz sistemi` olarak konumlandirilacaktir.

## Problem Tanimi

Gercek dunyada toplu tasima sistemleri surekli konum, hiz ve yolcu yogunlugu gibi veriler uretir. Bu verilerin anlik toplanmasi, bulutta islenmesi ve kullaniciya canli olarak gosterilmesi bulut bilisim ve gercek zamanli veri akisi konularinin temel uygulamalarindan biridir.

## Projenin Amaci

Bu projede sentetik otobus verisi uretilerek su yetenekler gosterilecektir:

- Gercek zamanli veri akisi
- MQTT ile veri iletimi
- AWS uzerinde veri isleme
- Verinin kalici olarak saklanmasi
- Canli izleme ve temel analiz gosterimi

## Neden Sentetik Veri

Proje kapsaminda gercek EGO entegrasyonu veya gercek paso verisi bulunmamaktadir. Bu nedenle sistem, gercek bir belediye entegrasyonunu taklit eden sentetik veri ile calisacaktir.

Bu tercih asagidaki acilardan mesrudur:

- Ders metni simulasyonu acikca kabul etmektedir
- Teknik odak veri kaynagi degil, veri akisinin islenmesidir
- Sentetik veri sayesinde kontrollu ve tekrarlanabilir demo uretilebilir

## Basari Kriterleri

Asagidaki kosullar saglanirsa proje basarili kabul edilir:

- Birden fazla otobus belirli araliklarla MQTT uzerinden veri gonderir
- Veri AWS uzerinde islenir
- Islenen veri DynamoDB'ye yazilir
- Dashboard anlik durum bilgisini gosterir
- Rapor ve video proje akisina uygun sekilde hazirlanir

## Not

Bu proje bir "gercek EGO entegrasyonu" olarak degil, "EGO-benzeri bir sistem simulasyonu" olarak anlatilacaktir.
