# visualization/palet_gorsellestirme.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Her ürün adı için sabit bir renk tanımlıyoruz.
ITEM_COLORS = {
    "Buzdolabı": "red",
    "Çamaşır Makinesi": "blue",
    "Televizyon": "green",
    "Mikrodalga": "yellow",
    "Koli": "orange",
    "Klima": "purple",
    "Mini Buzdolabı": "cyan",
    "Fırın": "magenta"
}

def ciz_3d_paletler(tum_paletler):
    """
    Her palet için ayrı 3D pencere açar. Aynı ürün adları (Buzdolabı, Klima vb.)
    aynı renk ile çizilir. Kenarları siyah çerçeveli görünmesi için edgecolor='black' ekliyoruz.
    """
    for i, palet in enumerate(tum_paletler, start=1):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for (urun, x, y, z) in palet.urunler:
            # Ürün adına bağlı sabit renk alıyoruz; 
            # sözlükte yoksa siyah (black) kullanıyoruz.
            color = ITEM_COLORS.get(urun.ad, "black")

            ax.bar3d(
                x, y, z,
                urun.genislik,
                urun.derinlik,
                urun.yukseklik,
                color=color,
                alpha=0.7,
                edgecolor="black",  # Kenar çizgisi
                linewidth=1,        # Kenar kalınlığı
                shade=False
            )

        ax.set_xlim(0, palet.genislik)
        ax.set_ylim(0, palet.derinlik)
        ax.set_zlim(0, palet.max_yukseklik)

        ax.set_title(f"Palet {i} - Mixed={palet.is_mixed}")
        ax.set_xlabel("Genişlik (cm)")
        ax.set_ylabel("Derinlik (cm)")
        ax.set_zlabel("Yükseklik (cm)")

        plt.show()
