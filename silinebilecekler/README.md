# Silinebilecekler

Bu klasor, repoda kalici tutulmayan veya tekrar uretilebilir dosyalar icin not birakir.

Bu repo sadeleştirilirken asagidaki gecici alanlar temizlendi:

- `build/`
  AWS dagitimi sirasinda olusan paketler, policy resolve dosyalari ve cihaz sertifikalari
- `output/`
  Yerel prova sirasinda uretilen log ve `jsonl` ciktilari
- `report/output/`
  PDF uretilirken olusan ara HTML dosyalari
- `__pdf_extract.txt`
  PDF okuma denemesi icin olusmus gecici metin dosyasi
- `report/final-report.pdf`
  Kopya rapor PDF'i; final surum kok dizindeki `final-report.pdf` olarak tutuluyor
- `report/build_report_html.py`
  Ara donusum denemesi; final uretim icin gerekli degil

Bu notun amaci, ileride repo tekrar kalabaliklasirsa hangi dosyalarin guvenle silinebilecegini acik bir yerde gostermektir.
