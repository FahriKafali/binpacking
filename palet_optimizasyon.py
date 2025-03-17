from collections import defaultdict
from palet_gorsellestirme import ciz_3d_paletler  # 3D palet çizim fonksiyonunu içe aktar

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
        self.genislik = genislik
        self.derinlik = derinlik
        self.max_yukseklik = max_yukseklik
        self.max_agirlik = max_agirlik
        self.urunler = []  

    def kalan_yukseklik(self):
        toplam_yukseklik = sum(urun.yukseklik for urun in self.urunler)
        return self.max_yukseklik - toplam_yukseklik

    def kalan_agirlik(self):
        toplam_agirlik = sum(urun.agirlik for urun in self.urunler)
        return self.max_agirlik - toplam_agirlik

    def urun_ekle(self, urun):
        if self.kalan_yukseklik() >= urun.yukseklik and self.kalan_agirlik() >= urun.agirlik:
            self.urunler.append(urun)
            return True
        return False

    def __repr__(self):
        return f"Palet: {len(self.urunler)} ürün, Kalan Yükseklik: {self.kalan_yukseklik()} cm, Kalan Ağırlık: {self.kalan_agirlik()} kg"

def palet_sec():
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

def urunleri_sirala(urun_listesi):
    kirilganlik_degerleri = {"Az": 0, "Orta": 1, "Çok": 2}
    return sorted(urun_listesi, key=lambda x: (-x.agirlik, kirilganlik_degerleri[x.kirilganlik]))

def urunleri_grupla(urun_listesi):
    gruplar = defaultdict(list)
    for urun in urun_listesi:
        gruplar[urun.ad].append(urun)
    return gruplar

def akilli_palete_yerlestir(urun_listesi, secilen_palet):
    """
    1) Aynı tip (adi) olan ürünleri gruplar.
    2) Her grupta mümkün olduğunca "normal palet" doldurur.
       - Eğer bir grup, tam dolacak kadar ürüne sahipse yeni normal palet açar.
       - Fakat arta kalan ufak sayıda ürün varsa bunları mix palete aktarır.
    3) Tüm gruplar işlendikten sonra kalan ürünleri ("kalan_urunler") mix paletlere yerleştirir.
       - Bu adımda farklı tip ürünler aynı mix palete gidebilir (kırılganlık, ağırlık vb. kontrollerle).
    4) Sonuç olarak "normal_paletler" ve "mix_paletler" listeleri döner.

    :param urun_listesi: Tüm ürünlerin listesi (Urun tipinde nesneler).
    :param secilen_palet: Bir Palet nesnesi; (genislik, derinlik, max_yukseklik, max_agirlik) gibi alanları var.
    :return: (normal_paletler, mix_paletler)
    """

    # 1) Ürünleri ada göre (tipine göre) grupla
    gruplar = urunleri_grupla(urun_listesi)  
    # Örn. {'Buzdolabı': [...], 'Mini Buzdolabı': [...], 'Çamaşır Makinesi': [...]}

    normal_paletler = []
    kalan_urunler = []

    # 2) Her ürün tipi için normal paletleri doldur
    for urun_adi, grup_listesi in gruplar.items():

        # Grupları isterseniz ağırlık/boyuta göre sıralayabilirsiniz. Örneğin en büyükten küçüğe:
        # (Bu opsiyonel; sadece paleti efektif doldurmaya yardımcı olabilir)
        grup_sirali = sorted(grup_listesi, key=lambda x: x.yukseklik * x.genislik * x.derinlik, reverse=True)

        # Palete ürün doldurmaya başlayacağız.
        index = 0
        toplam_urun_sayisi = len(grup_sirali)

        while index < toplam_urun_sayisi:
            # Yeni bir normal palet oluştur
            yeni_palet = Palet(
                genislik=secilen_palet.genislik,
                derinlik=secilen_palet.derinlik,
                max_yukseklik=secilen_palet.max_yukseklik,
                max_agirlik=secilen_palet.max_agirlik
            )

            # Palete sığdığı kadar ürün eklemeye çalış
            baslangic_index = index
            while index < toplam_urun_sayisi:
                urun = grup_sirali[index]
                if not yeni_palet.urun_ekle(urun):
                    # Ekleyemediysek bu palet artık dolmuş demektir.
                    break
                index += 1

            # Palete en az 1 ürün eklendiyse normal_paletler'e kaydediyoruz
            urun_eklenen_sayi = index - baslangic_index

            if urun_eklenen_sayi == 0:
                # Hiç ürün eklenemediyse, demek ki bu palete bu tip ürün sığmıyor. 
                # (Büyük ihtimalle boyut/ağırlık nedeniyle.)
                # Bu durumda kalan bütün ürünleri mix'e atmak mantıklı (çünkü normal paletlik bir durum yok).
                kalan_urunler.extend(grup_sirali[index:])
                break  # Bu ürün tipi için döngüyü kesiyoruz.

            # Paletimize ürün eklendi, normal_paletler listesine ekliyoruz.
            normal_paletler.append(yeni_palet)

            # Kalan ürün sayısı = grup_sirali kalan
            kalan_sayisi = toplam_urun_sayisi - index

            # --- BURASI ÖNEMLİ --- 
            # Eğer "kalan_sayisi" azsa ve muhtemelen yeni bir normal paleti tam dolduramayacaksak 
            # (ya da "ekonomik olmayacaksa"), bu kalanları MIX'e atıyoruz.
            # Kuralı siz belirleyin: Örneğin "kalan sayısı 2'den azsa" ya da "kalan ürünlerden 
            # bir palet daha tamamen dolmuyor" vb.

            # Örnek olarak: "Bir palet daha DOLACAK KADAR ürün yoksa" (yaklaşık yükseklik/ağırlık hesabına göre)
            # bunların hepsini mix'e at.
            # Bunu netleştirmek için basit bir yaklaşım:
            #    "Kalan ürün sayısı 2 veya 3ten azsa, onları mix palete gönder."

            # Tabii ki "tam dolacak kadar var mı?" kontrolü için paletin boyut/ağırlık kapasitesine
            # ve tek tek ürünlerin boyutuna/ağırlığına bakmak gerek. 
            # Ama burada basitçe, "az kaldıysa" mantığı gösteriyoruz.
            threshold = 2  # "2 üründen az kaldıysa, normal palet açmayalım" gibi

            if kalan_sayisi <= threshold:
                # Kalanları direkt mix'e at
                for _ in range(kalan_sayisi):
                    kalan_urunler.append(grup_sirali[index])
                    index += 1
                # Döngü biter
                break

            # Eğer kalanda yeterince ürün varsa, "while index < toplam_urun_sayisi" döngüsü devam eder,
            # yeni bir normal palet daha deneyeceğiz.

    # 3) Tüm ürün tipleri için normal paletler dolduruldu. 
    #    Şimdi arta kalanlar (kalan_urunler) var: bunları mix paletlere dağıtacağız.

    # Mix palet oluşturma mantığı:
    # - palet boyut/ağırlık limitleri 
    # - maksimum ürün sayısı (örneğin 4 ya da 5)
    # - kırılganlık durumuna dikkat (kırılganlığı çok olan ürünleri aynı palete koymak veya koymamak gibi)

    mix_paletler = []
    max_urun_mix_palet = 4  # Bir mix palete en fazla 4 ürün koyalım (örnek)

    # (Opsiyonel) Kırılgan ürünleri önce yerleştirmek isterseniz sıralayabilirsiniz.
    # Örneğin "çok kırılgan" > "orta" > "az" gibi. Burada basitçe geçiyoruz.
    for urun in kalan_urunler:
        yerlesti = False
        # Mevcut mix paletlere sığdırmaya çalış
        for mp in mix_paletler:
            if (mp.kalan_yukseklik() >= urun.yukseklik and
                mp.kalan_agirlik() >= urun.agirlik and
                len(mp.urunler) < max_urun_mix_palet):
                if mp.urun_ekle(urun):
                    yerlesti = True
                    break
        # Hiçbir mevcut mix palete sığmadıysa, yeni mix palet açıyoruz
        if not yerlesti:
            yeni_mix = Palet(
                genislik=secilen_palet.genislik,
                derinlik=secilen_palet.derinlik,
                max_yukseklik=secilen_palet.max_yukseklik,
                max_agirlik=secilen_palet.max_agirlik
            )
            eklendi = yeni_mix.urun_ekle(urun)
            if eklendi:
                mix_paletler.append(yeni_mix)
            else:
                # Yeni palete bile eklenemiyorsa, ürünü taşıyacak palet yok demektir.
                print(f"Uyarı: '{urun.adi}' ürünü hiçbir palete sığmıyor.")

    # 4) Sonuç olarak normal_paletler ve mix_paletler listelerini döndürüyoruz
    return normal_paletler, mix_paletler



# Daha az çeşit, ama fazla sayıda ürün içeren yeni liste
urunler = [
    Urun("Buzdolabı", 30, 30, 60, 180, "Az"),  
    Urun("Buzdolabı", 30, 30, 60, 180, "Az"),  
    Urun("Buzdolabı", 30, 30, 60, 180, "Az"),  
    Urun("Buzdolabı", 30, 30, 60, 180, "Az"),
    Urun("Buzdolabı", 30, 30, 60, 180, "Az"), 
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),  
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),  
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),  
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),  
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),  
    Urun("Çamaşır Makinesi", 30, 30, 45, 130, "Az"),    
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),  
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),  
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),  
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),  
    Urun("Televizyon", 50, 6, 25, 50, "Çok"),  
    Urun("Mikrodalga", 24, 24, 18, 35, "Orta"),  
    Urun("Mikrodalga", 24, 24, 18, 35, "Orta"),  
    Urun("Mikrodalga", 24, 24, 18, 35, "Orta"),  
    Urun("Mikrodalga", 24, 24, 18, 35, "Orta"),  
    Urun("Koli", 18, 18, 24, 30, "Az"),  
    Urun("Koli", 18, 18, 24, 30, "Az"),  
    Urun("Koli", 18, 18, 24, 30, "Az"),  
    Urun("Koli", 18, 18, 24, 30, "Az"),  
    Urun("Klima", 42, 21, 18, 80, "Orta"),  
    Urun("Klima", 42, 21, 18, 80, "Orta"),  
    Urun("Klima", 42, 21, 18, 80, "Orta"),  
    Urun("Klima", 42, 21, 18, 80, "Orta"),
    Urun("Klima", 42, 21, 18, 80, "Orta"),   
    Urun("Mini Buzdolabı", 30, 30, 50, 100, "Az"),  
    Urun("Mini Buzdolabı", 30, 30, 50, 100, "Az"),  
    Urun("Mini Buzdolabı", 30, 30, 50, 100, "Az"),  
    Urun("Mini Buzdolabı", 30, 30, 50, 100, "Az")
]



# Kullanıcıdan palet seçmesini iste
secilen_palet = palet_sec()

# Önce normal paletleme, sonra mix paletleme yap
normal_paletler, mix_paletler = akilli_palete_yerlestir(urunler, secilen_palet)

# Sonuçları ekrana yazdır
print("\n📦 **Normal Paletleme Sonucu:**")
for idx, palet in enumerate(normal_paletler, start=1):
    print(f"\nPalet {idx}:")
    print(palet)
    for urun in palet.urunler:
        print(f"  - {urun}")

print("\n📦 **Mix Paletleme Sonucu:**")
if mix_paletler:
    for idx, palet in enumerate(mix_paletler, start=1):
        print(f"\nMix Palet {idx}:")
        print(palet)
        for urun in palet.urunler:
            print(f"  - {urun}")
else:
    print("\n✔ Mix paletleme gerekli olmadı, tüm ürünler normal paletlere sığdı.")

ciz_3d_paletler(normal_paletler+mix_paletler)