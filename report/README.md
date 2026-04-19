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

PDF uretim scripti:

- `build_report_pdf.py`

## Onerilen Kullanim

En rahat yol:

1. `report/` klasorunu Overleaf'e yukle
2. `main.tex` dosyasini ana giris dosyasi yap
3. bolumleri sirasiyla doldur

Yerelde hazir PDF uretmek icin:

```powershell
.\.venv\Scripts\python.exe report/build_report_pdf.py
```

Bu komut PDF'yi repo kokune `final-report.pdf` olarak yazar.

Yerelde LaTeX kuruluysa tipik derleme sirasi:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Notlar

- Kapakta ders, ogrenci ve GitHub bilgileri guncellenmistir
- `main.tex` icindeki tarih teslim oncesi son kez kontrol edilmelidir
