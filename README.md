# WioKids

<p align="center">
  <img src="assets/logo.png" width="180" alt="WioKids">
</p>

CloudStream için Türkçe **çizgi film ve çocuk içerikleri** deposu.

## Aktif sağlayıcılar

| # | Sağlayıcı | Kaynak tipi |
|---:|---|---|
| 1 | ÇizgiMax | Çizgi film / animasyon |
| 2 | ÇizgiVeDizi | Çizgi film / dizi |
| 3 | Çizgi Portal | Çizgi dizi / animasyon film |
| 4 | ÇizgiFilmİzle Info | Geniş çizgi film arşivi |
| 5 | İzleOyna | Türkçe çizgi film |
| 6 | ÇizgiFilm TV | Çizgi film arşivi |
| 7 | ÇizgiDizi.net | Klasik ve güncel çizgi diziler |
| 8 | Çizgi Site | Türkçe çizgi film |
| 9 | Minika Çocuk | Resmî Minika Çocuk içeriği |
| 10 | Minika GO | Resmî Minika GO içeriği |

## YouTube fallback

**YouTube ayrı bir sağlayıcı değildir ve yukarıdaki 10 sayısına dahil değildir.**

Bir çizgi film veya bölüm oynatılırken WioKids önce ilgili sitenin kendi kaynaklarını çözer. Ardından içerik adı, bölüm adı ve varsa sezon/bölüm numarasıyla YouTube'da genel arama yapar. Yeterince eşleşen oynatılabilir sonuç varsa CloudStream'in YouTube extractor'ı üzerinden alternatif kaynak olarak eklenir.

Örnek: **Jetgiller → bölüm aç → site kaynakları + uygun YouTube sonucu**.

## Kurulum

CloudStream → Ayarlar → Eklentiler → Depo ekle:

https://raw.githubusercontent.com/Wiojelt/TurkSinema/wiokids/repo.json

plugins.json ana TurkSinema build'i her yayınlandığında otomatik olarak yalnız bu 10 sağlayıcıyla yenilenir.

made by **@Wiojelt**
