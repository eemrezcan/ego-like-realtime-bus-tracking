# Data Assets

Bu klasor, simulator ve isleme katmaninin kullanacagi temel veri dosyalarini tutar.

## Dosyalar

- `lines.json`: Hat bazli metadata
- `stops.json`: Durak tanimlari ve koordinatlar
- `routes.json`: Hatlarin durak sirasi ve segment bilgileri

## Tasarim Notlari

- Koordinatlar Ankara merkezini baz alan yaklasik ve sentetik degerlerdir
- Durak adlari EGO-benzeri bir his vermek icin secilmistir
- `routes.json` icindeki segment sureleri simulator ve ETA hesaplamasi icin temel referanstir
- `routes.json` tek bir yonun kanonik siralamasini tutar; ters yon bu siralamayi ters cevirerek elde edilir
