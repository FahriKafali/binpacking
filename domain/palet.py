class Palet:
    def __init__(self, genislik, derinlik, max_yukseklik, max_agirlik, is_mixed=False):
        self.genislik = genislik
        self.derinlik = derinlik
        self.max_yukseklik = max_yukseklik
        self.max_agirlik = max_agirlik
        self.is_mixed = is_mixed
        self.bos_alanlar = [(0, 0, 0, genislik, derinlik, max_yukseklik)]
        self.urunler = []

    def kalan_agirlik(self):
        toplam = sum(u.agirlik for (u, _, _, _) in self.urunler)
        return self.max_agirlik - toplam

    def uygun_bosluk_bul(self, urun):
        for i, (bx, by, bz, bw, bd, bh) in enumerate(self.bos_alanlar):
            if (urun.genislik <= bw) and (urun.derinlik <= bd) and (urun.yukseklik <= bh):
                return i, (bx, by, bz)
        return None, None

    def bosluklari_guncelle(self, urun, x, y, z):
        yeni_bosluklar = []
        for (bx, by, bz, bw, bd, bh) in self.bos_alanlar:
            if bx == x and by == y and bz == z \
               and bw >= urun.genislik and bd >= urun.derinlik and bh >= urun.yukseklik:
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
    # 1) Ağırlık kontrolü
        if self.kalan_agirlik() < urun.agirlik:
            return False  # Sığmadı

    # 2) Boyutsal kontrol
        result = self.uygun_bosluk_bul(urun)
        if not result or result[0] is None:
        # Hiç uygun boşluk bulunamadı
                return False

        index, (x, y, z) = result
        self.urunler.append((urun, x, y, z))
        self.bosluklari_guncelle(urun, x, y, z)
        return True


