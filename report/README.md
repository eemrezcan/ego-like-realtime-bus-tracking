# Final Report

Bu klasor, final proje raporunun IEEE-benzeri hibrit surumunu tutar.

Rapor yapisi:

- kapak sayfasi
- icindekiler
- iki sutunlu teknik govde
- IEEE numarali kaynakca

Ana dosya:

- `main.tex`

Alt bolumler:

- `sections/`

Kaynakca:

- `references.bib`

Sekiller:

- `figures/`

## Onerilen Kullanim

En rahat yol:

1. `report/` klasorunu Overleaf'e yukle
2. `main.tex` dosyasini ana giris dosyasi yap
3. bolumleri sirasiyla doldur

Yerelde LaTeX kuruluysa tipik derleme sirasi:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Notlar

- Kapakta ders ve ogrenci bilgileri guncellenmeli
- `main.tex` icindeki tarih ve kurum bilgileri teslim oncesi son kez kontrol edilmeli
- `figures/` klasorune mimari diyagrami ve ekran goruntuleri eklenmeli
