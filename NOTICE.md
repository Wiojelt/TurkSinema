# Kaynak, lisans ve atıf

TurkSinema aşağıdaki açık kaynak depoların seçili modüllerini tek CloudStream paketinde birleştirir:

## SalooRepo

- Depo: `https://github.com/Saloo1575/SalooRepo`
- Lisans: MIT
- Sabitlenen sürüm: `184deca182486d85388cffa5caf9ed1f53f387f3`
- Kullanılan modül sayısı: 30

## BronzeCloud / cloudstream-turkish

- Depo: `https://github.com/murattunc05/cloudstream-turkish`
- Lisans: GPL-3.0
- Sabitlenen sürüm: `a149da4e1a484357475b7b8bd54f6b2134924359`
- Kullanılan modül sayısı: 6

## Ripplay

- Depo: `https://github.com/Ripplay/cloudstream-repo`
- Lisans: GPL-3.0
- Sabitlenen sürüm: `e5251571a7c25482f9d046990a6e572b3b13c532`
- Kullanılan modül sayısı: 6

Paket; upstream bildirimlerinde geçen keyiflerolsun, JustRelaxable, usdogu, hexated, patron, nikyokki, SaurabhKaperwan, megix ve diğer katkıcıların çalışmalarını içerir. Ayrıntılı geçmiş ilgili upstream depolardadır.

GPL kapsamındaki kodla birleştiği için bütün türev paket GPL-3.0 altında yayımlanır. GitHub üzerinde açık bir yeniden kullanım lisansı bulunmayan incelenmiş depolardan kaynak kod alınmamıştır.

Yerel değişiklikler:

- Her modül çakışmaları önlemek için ayrı Kotlin ad alanına taşındı.
- Üç yedek sağlayıcı adı `Alternatif` ekiyle ayrıldı.
- CineStream giriş WebView'ında token kabulü beklenen alan adlarıyla sınırlandı.
- Cookie değeri logcat'e yazılmayacak biçimde maskeledi.
