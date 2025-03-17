import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def ciz_3d_paletler(paletler):
    """
    Paletleri ve içindeki ürünleri 3D olarak çizer.
    :param paletler: İçinde ürünlerin bulunduğu palet listesi
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    renkler = ["red", "blue", "green", "orange", "purple", "cyan", "yellow"]
    x_offset = 0  # Paletleri yan yana koymak için ofset

    for palet_index, palet in enumerate(paletler):
        y_offset = 0
        z_offset = 0

        # Paletin tabanını çiz (kahverengi, şeffaf)
        palet_kose_noktalari = np.array([
            [x_offset, y_offset, 0],
            [x_offset + palet.genislik, y_offset, 0],
            [x_offset + palet.genislik, y_offset + palet.derinlik, 0],
            [x_offset, y_offset + palet.derinlik, 0]
        ])
        ax.add_collection3d(Poly3DCollection([palet_kose_noktalari], color="brown", alpha=0.7))

        # Ürünleri yerleştir
        for urun in palet.urunler:
            renk = random.choice(renkler)

            # Ürünün köşe noktaları (x, y, z)
            urun_kose_noktalari = np.array([
                [x_offset, y_offset, z_offset],
                [x_offset + urun.genislik, y_offset, z_offset],
                [x_offset + urun.genislik, y_offset + urun.derinlik, z_offset],
                [x_offset, y_offset + urun.derinlik, z_offset],
                [x_offset, y_offset, z_offset + urun.yukseklik],
                [x_offset + urun.genislik, y_offset, z_offset + urun.yukseklik],
                [x_offset + urun.genislik, y_offset + urun.derinlik, z_offset + urun.yukseklik],
                [x_offset, y_offset + urun.derinlik, z_offset + urun.yukseklik]
            ])

            # Ürünün tüm yüzeylerini çiz
            faces = [
                [urun_kose_noktalari[j] for j in [0, 1, 2, 3]],  # Alt yüzey
                [urun_kose_noktalari[j] for j in [4, 5, 6, 7]],  # Üst yüzey
                [urun_kose_noktalari[j] for j in [0, 1, 5, 4]],  # Ön yüzey
                [urun_kose_noktalari[j] for j in [2, 3, 7, 6]],  # Arka yüzey
                [urun_kose_noktalari[j] for j in [1, 2, 6, 5]],  # Sağ yüzey
                [urun_kose_noktalari[j] for j in [4, 7, 3, 0]]   # Sol yüzey
            ]
            ax.add_collection3d(Poly3DCollection(faces, color=renk, alpha=0.5))

            # Yeni ürün için yer aç (yan yana diz)
            y_offset += urun.derinlik
            if y_offset >= palet.derinlik:
                y_offset = 0
                z_offset += urun.yukseklik

        # Bir sonraki paleti çizmek için X ekseninde kaydır
        x_offset += palet.genislik + 20

    # 3D eksenleri ayarla
    ax.set_xlabel("Genişlik (cm)")
    ax.set_ylabel("Derinlik (cm)")
    ax.set_zlabel("Yükseklik (cm)")
    ax.set_title("3D Palet Görselleştirme")

    # Görselleştirme
    plt.show()