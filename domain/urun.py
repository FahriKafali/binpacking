class Urun:
    KIRILGANLIK_SEVIYELERI = {"Az": 0, "Orta": 1, "Çok": 2}

    def __init__(self, ad, genislik, derinlik, yukseklik, agirlik, kirilganlik):
        if kirilganlik not in self.KIRILGANLIK_SEVIYELERI:
            raise ValueError("Kırılganlık 'Az', 'Orta' veya 'Çok' olmalıdır.")
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
