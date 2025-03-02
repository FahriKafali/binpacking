import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def ciz_3d_paletler(paletler):
    """
    Tüm paletleri ve içindeki ürünleri 3D olarak çizer.
    :param paletler: Paletlerin listesi, her biri içindeki ürünlerle birlikte.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Palet boyutları
    palet_genislik, palet_derinlik, palet_yukseklik = 120, 100, 180  # Örnek boyutlar

    # Paletleri çizmeye başla
    for idx, palet in enumerate(paletler):
        x_offset = idx * (palet_genislik + 20)  # Paletler arasında boşluk bırak

        # Palet tabanını çiz
        palet_kose_noktalari = np.array([
            [x_offset, 0, 0], [x_offset + palet_genislik, 0, 0],
            [x_offset + palet_genislik, palet_derinlik, 0], [x_offset, palet_derinlik, 0]
        ])
        ax.add_collection3d(Poly3DCollection([palet_kose_noktalari], color="brown", alpha=0.7))

        yukseklik = 0
        for urun in palet.urunler:
            urun_kose_noktalari = np.array([
                [x_offset, 0, yukseklik], [x_offset + urun.genislik, 0, yukseklik],
                [x_offset + urun.genislik, urun.derinlik, yukseklik], [x_offset, urun.derinlik, yukseklik]
            ])
            ax.add_collection3d(Poly3DCollection([urun_kose_noktalari], color="blue", alpha=0.5))
            yukseklik += urun.yukseklik  # Üst üste koymak için

    # Eksenleri ayarla
    ax.set_xlabel("Genişlik (cm)")
    ax.set_ylabel("Derinlik (cm)")
    ax.set_zlabel("Yükseklik (cm)")
    ax.set_title("3D Palet Görselleştirme")

    plt.show()
