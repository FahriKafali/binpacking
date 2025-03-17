from collections import defaultdict
from domain.palet import Palet

def yerlesim(urun_listesi, palet_info):
    gruplar = defaultdict(list)
    for u in urun_listesi:
        gruplar[u.ad].append(u)

    single_type_paletler = []
    leftover = []

    for urun_adi, grup in gruplar.items():
        p = Palet(
            palet_info["genislik"],
            palet_info["derinlik"],
            palet_info["max_yukseklik"],
            palet_info["max_agirlik"],
            is_mixed=False
        )
        for urun in grup:
            if not p.urun_ekle(urun):
                leftover.append(urun)
        if p.urunler:
            single_type_paletler.append(p)

    leftover.sort(key=lambda x: x.kirilganlik_seviyesi())
    mix_paletler = []

    for urun in leftover:
        eklendi = False
        for mp in mix_paletler:
            if mp.urun_ekle(urun):
                eklendi = True
                break
        if not eklendi:
            mp_new = Palet(
                palet_info["genislik"],
                palet_info["derinlik"],
                palet_info["max_yukseklik"],
                palet_info["max_agirlik"],
                is_mixed=True
            )
            mp_new.urun_ekle(urun)
            mix_paletler.append(mp_new)

    return single_type_paletler, mix_paletler
