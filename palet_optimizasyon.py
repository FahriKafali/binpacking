class Urun:
    KIRILGANLIK_SEVIYELERI = {
        "Az": 0,  # En sağlam ürünler
        "Orta": 1,  
        "Çok": 2   # En kırılgan ürünler
    }

    def __init__(self, ad, genislik, derinlik, yukseklik, agirlik, kirilganlik):
        """
        Ürün bilgilerini içeren sınıf.
        :param ad: Ürünün adı
        :param genislik: Ürünün genişliği (cm)
        :param derinlik: Ürünün derinliği (cm)
        :param yukseklik: Ürünün yüksekliği (cm)
        :param agirlik: Ürünün ağırlığı (kg)
        :param kirilganlik: Ürünün kırılganlık seviyesi ("Az", "Orta", "Çok")
        """
        if kirilganlik not in self.KIRILGANLIK_SEVIYELERI:
            raise ValueError("Kırılganlık seviyesi 'Az', 'Orta' veya 'Çok' olmalıdır.")
        
        self.ad = ad
        self.genislik = genislik
        self.derinlik = derinlik
        self.yukseklik = yukseklik
        self.agirlik = agirlik
        self.kirilganlik = kirilganlik  # Metin olarak saklanacak

    def __repr__(self):
        return f"{self.ad} ({self.genislik}x{self.derinlik}x{self.yukseklik} cm, {self.agirlik} kg, Kırılganlık: {self.kirilganlik})"
# 4 Farklı Standart Palet Tanımı
PALET_TIPLERI = {
    1: {"ad": "Avrupa Paleti (EUR-Palet)", "genislik": 120, "derinlik": 80, "max_yukseklik": 180, "max_agirlik": 1500},
    2: {"ad": "ISO Standart Palet", "genislik": 120, "derinlik": 100, "max_yukseklik": 200, "max_agirlik": 2000},
    3: {"ad": "Asya Paleti", "genislik": 110, "derinlik": 110, "max_yukseklik": 190, "max_agirlik": 1800},
    4: {"ad": "ABD Paleti (GMA Palet)", "genislik": 121.9, "derinlik": 101.6, "max_yukseklik": 200, "max_agirlik": 2500}
}


class Palet:
    def __init__(self, genislik, derinlik, max_yukseklik, max_agirlik):
        """
        Palet sınıfı: Ürünlerin yerleştirildiği platform.
        :param genislik: Paletin genişliği (cm)
        :param derinlik: Paletin derinliği (cm)
        :param max_yukseklik: Maksimum yükseklik (cm)
        :param max_agirlik: Maksimum ağırlık (kg)
        """
        self.genislik = genislik
        self.derinlik = derinlik
        self.max_yukseklik = max_yukseklik
        self.max_agirlik = max_agirlik
        self.urunler = []  # Palete eklenen ürünler

    def kalan_yukseklik(self):
        """Palette kalan yükseklik miktarını döndürür."""
        toplam_yukseklik = sum(urun.yukseklik for urun in self.urunler)
        return self.max_yukseklik - toplam_yukseklik

    def kalan_agirlik(self):
        """Palette kalan ağırlık kapasitesini döndürür."""
        toplam_agirlik = sum(urun.agirlik for urun in self.urunler)
        return self.max_agirlik - toplam_agirlik

    def urun_ekle(self, urun):
        """Ürünü palete ekler, eğer sınırları aşmıyorsa."""
        if self.kalan_yukseklik() >= urun.yukseklik and self.kalan_agirlik() >= urun.agirlik:
            self.urunler.append(urun)
            return True
        return False

    def __repr__(self):
        return f"Palet: {len(self.urunler)} ürün, Kalan Yükseklik: {self.kalan_yukseklik()} cm, Kalan Ağırlık: {self.kalan_agirlik()} kg"


class Konteyner:
    def __init__(self, genislik=240, derinlik=220, yukseklik=260, max_agirlik=20000):
        """
        Konteyner sınıfı: Paletlerin içine yerleştirileceği büyük depo alanı.
        :param genislik: Konteyner genişliği (cm)
        :param derinlik: Konteyner derinliği (cm)
        :param yukseklik: Konteyner yüksekliği (cm)
        :param max_agirlik: Maksimum ağırlık kapasitesi (kg)
        """
        self.genislik = genislik
        self.derinlik = derinlik
        self.yukseklik = yukseklik
        self.max_agirlik = max_agirlik
        self.paletler = []  # Konteyner içine yerleştirilen paletler

    def palet_ekle(self, palet):
        """Paleti konteynere ekler, eğer sınırları aşmıyorsa."""
        toplam_agirlik = sum(p.max_agirlik for p in self.paletler)
        if toplam_agirlik + palet.max_agirlik <= self.max_agirlik:
            self.paletler.append(palet)
            return True
        return False

    def __repr__(self):
        return f"Konteyner: {len(self.paletler)} palet, Maksimum Ağırlık: {self.max_agirlik} kg"
def palet_sec():
    """Kullanıcının 4 standart palet tipinden birini seçmesini sağlar."""
    print("Lütfen bir palet tipi seçiniz:")
    for key, value in PALET_TIPLERI.items():
        print(f"{key}. {value['ad']} - {value['genislik']}x{value['derinlik']} cm, Maks. Yükseklik: {value['max_yukseklik']} cm, Maks. Ağırlık: {value['max_agirlik']} kg")
    
    while True:
        try:
            secim = int(input("Seçiminizi yapınız (1-4): "))
            if secim in PALET_TIPLERI:
                secilen_palet = PALET_TIPLERI[secim]
                print(f"\n{secilen_palet['ad']} seçildi!\n")
                return Palet(
                    genislik=secilen_palet["genislik"],
                    derinlik=secilen_palet["derinlik"],
                    max_yukseklik=secilen_palet["max_yukseklik"],
                    max_agirlik=secilen_palet["max_agirlik"]
                )
            else:
                print("Lütfen 1 ile 4 arasında bir seçim yapınız.")
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı giriniz.")

# Kullanıcının palet seçmesini sağla
secilen_palet = palet_sec()
print(secilen_palet)

from collections import defaultdict

def urunleri_grupla(urun_listesi):
    """
    Aynı tür ürünleri bir araya gruplar.
    :param urun_listesi: Tüm ürünlerin listesi
    :return: Gruplanmış ürünlerin bir sözlüğü (anahtar: ürün adı, değer: aynı üründen oluşan liste)
    """
    gruplar = defaultdict(list)
    for urun in urun_listesi:
        gruplar[urun.ad].append(urun)  # Aynı isimli ürünleri bir araya getir
    return gruplar

def ayni_tur_palete_yerlestir(urun_listesi, secilen_palet):
    """
    Aynı türdeki ürünleri tek palete yerleştirir.
    Eğer ürünler palet kapasitesini aşarsa, yeni bir palet açar.
    :param urun_listesi: Yerleştirilecek ürünlerin listesi
    :param secilen_palet: Kullanıcının seçtiği palet
    :return: Yerleştirilen paletlerin listesi
    """
    paletler = []
    gruplu_urunler = urunleri_grupla(urun_listesi)  # Aynı tür ürünleri grupla

    for urun_adi, grup in gruplu_urunler.items():
        mevcut_palet = None

        for urun in grup:
            if mevcut_palet is None or not mevcut_palet.urun_ekle(urun):
                # Eğer mevcut palete eklenemezse, yeni bir palet oluştur
                mevcut_palet = Palet(
                    genislik=secilen_palet.genislik,
                    derinlik=secilen_palet.derinlik,
                    max_yukseklik=secilen_palet.max_yukseklik,
                    max_agirlik=secilen_palet.max_agirlik
                )
                mevcut_palet.urun_ekle(urun)
                paletler.append(mevcut_palet)

    return paletler  # Paletlerin listesi döndürülür
# Örnek ürün listesi
urunler = [
    Urun("Buzdolabı", 60, 60, 180, 70, "Az"),  # Dayanıklı (Az)
    Urun("Buzdolabı", 60, 60, 180, 70, "Az"),  # Dayanıklı (Az)
    Urun("Çamaşır Makinesi", 60, 60, 85, 65, "Az"),  # Dayanıklı (Az)
    Urun("Çamaşır Makinesi", 60, 60, 85, 65, "Az"),  # Dayanıklı (Az)
    Urun("Televizyon", 100, 10, 60, 20, "Çok"),  # Kırılgan (Çok)
    Urun("Televizyon", 100, 10, 60, 20, "Çok"),  # Kırılgan (Çok)
    Urun("Mikrodalga", 50, 50, 30, 15, "Orta"),  # Orta kırılganlık
    Urun("Koli", 40, 40, 40, 10, "Az"),  # Dayanıklı (Az)
    Urun("Koli", 40, 40, 40, 10, "Az"),  # Dayanıklı (Az)
    Urun("Koli", 40, 40, 40, 10, "Az")   # Dayanıklı (Az)
]


# Kullanıcıdan palet seçmesini iste
secilen_palet = palet_sec()

# Seçilen palete göre aynı türdeki ürünleri yerleştir
paletler = ayni_tur_palete_yerlestir(urunler, secilen_palet)

# Sonuçları ekrana yazdır
print("\nPaletleme Sonucu:")
for idx, palet in enumerate(paletler, start=1):
    print(f"\nPalet {idx}:")
    print(palet)
    for urun in palet.urunler:
        print(f"  - {urun}")
