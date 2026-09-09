# TurkSinema — Nuvio Desktop

Mevcut CloudStream eklentilerini [CNCVerse Bridge Windows](https://github.com/NivinCNC/CNCVerse-Bridge/releases/latest) üzerinden kullanabilirsin. CloudStream kurulumu ve paketleri değişmez.

1. Bridge'i kurup aç.
2. Bridge'in depo yönetimine aşağıdaki adresi ekle; istediğin sağlayıcıları yükle:

```text
https://raw.githubusercontent.com/Wiojelt/TurkSinema/main/nuvio.json
```

3. Bridge sunucusunu başlat. Gösterdiği addon adresini **Nuvio Desktop → Eklentiler / Addons** alanına ekle. Aynı bilgisayarda varsayılan örnek:

```text
http://127.0.0.1:8080/manifest.json
```

Bridge farklı port gösteriyorsa onun adresini kullan. Nuvio kullanılırken Bridge açık kalmalıdır.

**nuvio.json Bridge'e eklenir; doğrudan Nuvio JavaScript plugin veya Stremio manifesti değildir.** GitHub tek başına Kotlin eklentilerini çalıştırmaz. Nuvio'ya eklenecek çalışan manifesti Bridge üretir.

Kaynak listesi mevcut CloudStream builds listesinden gelir; iki sistem aynı paket güncellemelerini kullanır. Bridge altında tüm sağlayıcılar test edilmemiştir. Windows'ta WebView isteyen kaynaklar ve bazı Android'e özel ayar ekranları çalışmayabilir.

[Bridge'in resmî kullanım açıklaması](https://github.com/NivinCNC/CNCVerse-Bridge/blob/main/README.md)
