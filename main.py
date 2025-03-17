import os
from domain.urun import Urun
from services.yerlesim import yerlesim
from visualization.palet_gorsellestirme import ciz_3d_paletler

PALET_TIPLERI = {
    1: {"ad": "Avrupa Paleti", "genislik": 120,   "derinlik": 80,  "max_yukseklik": 180, "max_agirlik": 1500},
    2: {"ad": "ISO Standart",  "genislik": 120,   "derinlik": 100, "max_yukseklik": 200, "max_agirlik": 2000},
    3: {"ad": "Asya Paleti",   "genislik": 110,   "derinlik": 110, "max_yukseklik": 190, "max_agirlik": 1800},
    4: {"ad": "ABD Paleti",    "genislik": 121.9, "derinlik":101.6,"max_yukseklik": 200, "max_agirlik": 2500}
}

def urunleri_dosyadan_oku(dosya_yolu):
    urun_listesi = []
    if not os.path.exists(dosya_yolu):
        print("Dosya bulunamadı:", dosya_yolu)
        return urun_listesi

    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        for satir in f:
            satir = satir.strip()
            if not satir:
                continue
            parts = satir.split(',')
            if len(parts) != 6:
                print("Geçersiz satır:", satir)
                continue

            ad  = parts[0]
            gen = float(parts[1])
            der = float(parts[2])
            yuk = float(parts[3])
            agi = float(parts[4])
            kir = parts[5]

            urun = Urun(ad, gen, der, yuk, agi, kir)
            urun_listesi.append(urun)

    return urun_listesi

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

if __name__ == "__main__":
    # 1) Ürünleri dosyadan oku
    dosya_yolu = "data/urun_listesi.txt"
    urunler = urunleri_dosyadan_oku(dosya_yolu)

    if not urunler:
        print("Ürün listesi boş veya dosya yok. Program sonlanıyor.")
        exit(0)

    # 2) Palet seç
    palet_info = palet_sec()

    # 3) Yerleştir
    single_paletler, mix_paletler = yerlesim(urunler, palet_info)

    # 4) Yazdır
    print("\n📦 **Tek Çeşit Paletler:**")
    for i, palet in enumerate(single_paletler, start=1):
        print(f"\nPalet {i} (is_mixed={palet.is_mixed}):")
        for (urun, _, _, _) in palet.urunler:
            print("   *", urun)
        print("Kalan Ağırlık:", palet.kalan_agirlik(), "kg")

    print("\n📦 **Mix Paletler:**")
    if mix_paletler:
        for i, palet in enumerate(mix_paletler, start=1):
            print(f"\nMix Palet {i} (is_mixed={palet.is_mixed}):")
            for (urun, _, _, _) in palet.urunler:
                print("   *", urun)
            print("Kalan Ağırlık:", palet.kalan_agirlik(), "kg")
    else:
        print("Hiç leftover ürün yok, dolayısıyla mix palet de yok.")

    # 5) 3D Çizim
    tum_paletler = single_paletler + mix_paletler
    ciz_3d_paletler(tum_paletler)
