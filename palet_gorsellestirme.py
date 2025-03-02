import matplotlib.pyplot as plt 
import numpy as np 
from mpl_toolkits.mplot3d.art3d import Poly3DCollection 

def ciz_3d_paletler(paletler):
    """
    Tüm paletleri ve içindeki ürünleri 3D olarak çizer.
    :param paletler: Paletlerin listesi, her biri içindeki ürünlerle birlikte gösterilir.
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    palet_genislik, palet_derinlik, palet_yukseklik = 120, 100, 15  # Standart palet boyutları

    x_offset = 0
    y_offset = 0

    for idx, palet in enumerate(paletler):
        # Palet tabanı
        palet_koordinatlar = [
            [x_offset, y_offset, 0],
            [x_offset + palet_genislik, y_offset, 0],
            [x_offset + palet_genislik, y_offset + palet_derinlik, 0],
            [x_offset, y_offset + palet_derinlik, 0]
        ]
        ax.add_collection3d(Poly3DCollection([palet_koordinatlar], color="brown", alpha=0.5))

        # Ürünleri üst üste yerleştirerek göster
        urun_z_offset = palet_yukseklik  

        for urun in palet.urunler:
            urun_koordinatlar = [
                [x_offset, y_offset, urun_z_offset],
                [x_offset + urun.genislik, y_offset, urun_z_offset],
                [x_offset + urun.genislik, y_offset + urun.derinlik, urun_z_offset],
                [x_offset, y_offset + urun.derinlik, urun_z_offset],
            ]
            ax.add_collection3d(Poly3DCollection([urun_koordinatlar], color=np.random.rand(3,), alpha=0.7))
            urun_z_offset += urun.yukseklik + 2  

        # Yeni paleti bir sonraki sıraya koy
        x_offset += palet_genislik + 20  
        if (idx + 1) % 4 == 0:  
            x_offset = 0
            y_offset += palet_derinlik + 20

    ax.set_xlabel("Genişlik (cm)")
    ax.set_ylabel("Derinlik (cm)")
    ax.set_zlabel("Yükseklik (cm)")
    ax.set_title("3D Paletler ve Ürün Yerleşimi")
    ax.set_xlim([0, x_offset + palet_genislik])
    ax.set_ylim([0, y_offset + palet_derinlik])
    ax.set_zlim([0, 250])

    plt.show()
