from collections import defaultdict

class Urun:
    KIRILGANLIK_SEVIYELERI = {"Az": 0, "Orta": 1, "Çok": 2}

    def __init__(self, ad, genislik, derinlik, yukseklik, agirlik, kirilganlik):
        if kirilganlik not in self.KIRILGANLIK_SEVIYELERI:
            raise ValueError("Kırılganlık seviyesi 'Az', 'Orta' veya 'Çok' olmalıdır.")
        self.ad = ad
        self.genislik = genislik
        self.derinlik = derinlik
        self.yukseklik = yukseklik
        self.agirlik = agirlik
        self.kirilganlik = kirilganlik

    def kirilganlik_seviyesi(self):
        return self.KIRILGANLIK_SEVIYELERI[self.kirilganlik]

    def __repr__(self):
        return (f"{self.ad} ({self.genislik}x{self.derinlik}x{self.yukseklik} cm, "
                f"{self.agirlik} kg, Kırılganlık: {self.kirilganlik})")


class Palet:
    def __init__(self, genislik, derinlik, max_yukseklik, max_agirlik, is_mixed=False):
        self.genislik = genislik
        self.derinlik = derinlik
        self.max_yukseklik = max_yukseklik
        self.max_agirlik = max_agirlik
        self.is_mixed = is_mixed
        # Başlangıçta paletin tamamı tek parça boş alan
        self.bos_alanlar = [(0, 0, 0, genislik, derinlik, max_yukseklik)]
        self.urunler = []  # (Urun, x, y, z)

    def kalan_agirlik(self):
        return self.max_agirlik - sum(u.agirlik for u, _, _, _ in self.urunler)

    def uygun_bosluk_bul(self, urun):
        for i, (bx, by, bz, bw, bd, bh) in enumerate(self.bos_alanlar):
            if (urun.genislik <= bw) and (urun.derinlik <= bd) and (urun.yukseklik <= bh):
                return i, (bx, by, bz)
        return None, None

    def bosluklari_guncelle(self, urun, x, y, z):
        yeni_bosluklar = []
        for (bx, by, bz, bw, bd, bh) in self.bos_alanlar:
            if bx == x and by == y and bz == z and bw >= urun.genislik and bd >= urun.derinlik and bh >= urun.yukseklik:
                # 3 parçaya böl
                if urun.genislik < bw:
                    yeni_bosluklar.append((x + urun.genislik, y, z, bw - urun.genislik, bd, bh))
                if urun.derinlik < bd:
                    yeni_bosluklar.append((x, y + urun.derinlik, z, bw, bd - urun.derinlik, bh))
                if urun.yukseklik < bh:
                    yeni_bosluklar.append((x, y, z + urun.yukseklik, bw, bd, bh - urun.yukseklik))
            else:
                yeni_bosluklar.append((bx, by, bz, bw, bd, bh))

        self.bos_alanlar = yeni_bosluklar

    def urun_ekle(self, urun):
        # Ağırlık kontrolü
        if self.kalan_agirlik() < urun.agirlik:
            return False

        index, (x, y, z) = self.uygun_bosluk_bul(urun)
        if index is not None:
            self.urunler.append((urun, x, y, z))
            self.bosluklari_guncelle(urun, x, y, z)
            return True
        return False


PALET_TIPLERI = {
    1: {"ad": "Avrupa Paleti", "genislik":120, "derinlik":80,  "max_yukseklik":180, "max_agirlik":1500},
    2: {"ad": "ISO Standart",  "genislik":120, "derinlik":100, "max_yukseklik":200, "max_agirlik":2000},
    3: {"ad": "Asya Paleti",   "genislik":110, "derinlik":110, "max_yukseklik":190, "max_agirlik":1800},
    4: {"ad": "ABD Paleti",    "genislik":121.9, "derinlik":101.6, "max_yukseklik":200, "max_agirlik":2500}
}


def palet_sec():
    print("Lütfen bir palet tipi seçiniz:")
    for key, value in PALET_TIPLERI.items():
        print(f"{key}. {value['ad']} - {value['genislik']}x{value['derinlik']} cm, "
              f"Maks. Yükseklik: {value['max_yukseklik']} cm, Maks. Ağırlık: {value['max_agirlik']} kg")

    while True:
        try:
            secim = int(input("Seçiminizi yapınız (1-4): "))
            if secim in PALET_TIPLERI:
                return PALET_TIPLERI[secim]
            else:
                print("Lütfen 1 ile 4 arasında bir seçim yapınız.")
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı giriniz.")


def yerlesim(urun_listesi, palet_info):
    """
    Aşama 1: Tek-çeşit palet (her gruba sadece 1 tane açıyoruz), sığmayanlar leftover.
    Aşama 2: Leftover ürünler mix palet(ler) olarak ekrana gelecek.
    """
    from collections import defaultdict

    gruplar = defaultdict(list)
    for u in urun_listesi:
        gruplar[u.ad].append(u)

    single_type_paletler = []
    leftover = []

    # -- AŞAMA 1: Tek palet (her grup için 1) --
    for urun_adi, grup in gruplar.items():
        palet = Palet(
            palet_info["genislik"],
            palet_info["derinlik"],
            palet_info["max_yukseklik"],
            palet_info["max_agirlik"],
            is_mixed=False
        )
        for u in grup:
            if not palet.urun_ekle(u):
                leftover.append(u)  # sığmadı
        if palet.urunler:
            single_type_paletler.append(palet)

    # -- AŞAMA 2: Leftover -> Mix Palet(ler) --
    leftover.sort(key=lambda x: x.kirilganlik_seviyesi())  # Az->Orta->Çok
    mix_paletler = []

    for urun in leftover:
        eklendi = False
        for mp in mix_paletler:
            if mp.urun_ekle(urun):
                eklendi = True
                break
        if not eklendi:
            yeni = Palet(
                palet_info["genislik"],
                palet_info["derinlik"],
                palet_info["max_yukseklik"],
                palet_info["max_agirlik"],
                is_mixed=True
            )
            yeni.urun_ekle(urun)
            mix_paletler.append(yeni)

    return single_type_paletler, mix_paletler


if __name__ == "__main__":

    # Burada ürünleri öyle miktarlarda ayarlıyoruz ki
    # her gruptan bir tek palet asla yeterli olmasın
    # (ki leftover oluşsun, leftover da mix paletlerde karışsın).

    urunler = [
        # Buzdolabı, 180 kg, 8 taneden sonra tek palet dolacak; geri kalan leftover
        *[Urun("Buzdolabı", 30, 30, 60, 180, "Az") for _ in range(12)],
        # Çamaşır Makinesi, 130 kg, 11 taneye kadar sığar, 12.yi leftover yapalım
        *[Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az") for _ in range(12)],
        # Televizyon, 50 kg, bir palet 30'a kadar alır, biz 35 tane koyalım
        *[Urun("Televizyon", 50, 6, 25, 50, "Çok") for _ in range(35)],
        # Mikrodalga, 35 kg, bir palet 42 tane alabilir ama biz 15 tane koyalım (bakalım leftover yaratacak mı)
        *[Urun("Mikrodalga", 24, 24, 18, 35, "Orta") for _ in range(15)],
        # Koli, 30 kg, bir palet 50 tane alabilir, 20 tane koyalım (muhtemelen leftover olmayacak)
        *[Urun("Koli", 18, 18, 24, 30, "Az") for _ in range(20)],
        # Klima, 80 kg, bir palet 18 taneyi sığdırır, 25 tane koyarsak leftover olur
        *[Urun("Klima", 42, 21, 18, 80, "Orta") for _ in range(25)],
        # Mini Buzdolabı, 100 kg, bir palet 15 taneyi sığdırır, 18 tane ekleyelim
        *[Urun("Mini Buzdolabı", 30, 30, 50, 100, "Az") for _ in range(18)],
        # Fırın, 90 kg, bir palet 16 taneyi sığdırır, 20 tane ekleyelim
        *[Urun("Fırın", 40, 40, 35, 90, "Orta") for _ in range(20)],
    ]

    palet_info = palet_sec()
    single, mix = yerlesim(urunler, palet_info)

    # Ekrana yazdırma
    print("\n📦 **Tek Çeşit Paletler:**")
    for i, palet in enumerate(single, start=1):
        print(f"\nPalet {i} (is_mixed={palet.is_mixed}):")
        for (urun, _, _, _) in palet.urunler:
            print(f"   * {urun}")
        print("Kalan Ağırlık:", palet.kalan_agirlik(), "kg")

    print("\n📦 **Mix Paletler:**")
    if mix:
        for i, palet in enumerate(mix, start=1):
            print(f"\nMix Palet {i} (is_mixed={palet.is_mixed}):")
            for (urun, _, _, _) in palet.urunler:
                print(f"   * {urun}")
            print("Kalan Ağırlık:", palet.kalan_agirlik(), "kg")
    else:
        print("Hiç leftover (artan ürün) yok, mix palet oluşmadı!")
