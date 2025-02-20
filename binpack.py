import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import pandas as pd


def get_user_input():
    
    print("\n Konteyner Hacim Bilgisi \n")
    konteyner_genislik = float(input("Konteyner genişliği: "))
    konteyner_yükseklik = float(input("Konteyner yüksekliği: "))
    konteyner_derinlik = float(input("Konteyner derinliği: "))
    
    print("\n Kutu Bilgisi \n")
    boxes = []
    counter_boxes = int(input("Kaç kutu eklemek istiyorsunuz: "))

    for i in range(counter_boxes):
        w = float(input(f"{i+1}. Kutunun genişliği: "))
        h = float(input(f"{i+1}. Kutunun yüksekliği: "))
        d = float(input(f"{i+1}. Kutunun derinliği: "))
        boxes.append((w, h, d))
    
    return (konteyner_genislik, konteyner_yükseklik, konteyner_derinlik), boxes


def choose_algorithm():
    
 while True:
    print("\n Yerleştirme algoritması seçin: ")
    print(" 1️ - First Fit Decreasing (FFD)")
    print(" 2️ - Best Fit Decreasing (BFD)")
    print(" 3️ - Genetic Algorithm (GA)")
    print(" 0 - Çıkış")
    
    try:
        secim = int(input("Seçiminizi yapın: "))
        if secim in [1, 2, 3]:
            return secim
        elif secim == 0:
         print("Çıkış Yapılıyor")
         break
        else:
         print(" Geçersiz seçim, lütfen 1, 2, 3 veya 0 girin!! ")
    except ValueError:
        print("Geçerli Sayı giriniz!")

def first_fit_decreasing(boxes, container):
    container_w, container_h, container_d = container
    placements = []  # Kutuların yerleşim bilgisi

    # 📌 Kutuları büyükten küçüğe sıralıyoruz
    boxes.sort(key=lambda b: b[0] * b[1] * b[2], reverse=True)

    # 📌 Mevcut boş alanları takip edelim
    free_spaces = [(0, 0, 0, container_w, container_h, container_d)]  # (x, y, z, w, h, d)

    for box in boxes:
        box_w, box_h, box_d = box
        placed = False  # Kutu yerleşti mi?

        # 📌 İlk uygun boşluğu bul
        for i, (x, y, z, free_w, free_h, free_d) in enumerate(free_spaces):
            if box_w <= free_w and box_h <= free_h and box_d <= free_d:  # Sığabiliyor mu?
                # 📌 Kutuyu yerleştir
                placements.append({'box': box, 'position': (x, y, z)})
                placed = True

                # 📌 Kalan boşlukları ekleyelim
                free_spaces.append((x + box_w, y, z, free_w - box_w, free_h, free_d))  # Sağ boşluk
                free_spaces.append((x, y + box_h, z, box_w, free_h - box_h, free_d))  # Alt boşluk
                free_spaces.append((x, y, z + box_d, box_w, box_h, free_d - box_d))  # Derinlik boşluğu

                # 📌 Mevcut boşluğu listeden kaldır
                del free_spaces[i]
                break  # İlk boşluğu bulduk, devam etmeye gerek yok

        if not placed:
            print(f"❌ Konteyner dolu! {box} kutusu yerleştirilemedi.")

    return placements



def best_fit_decreasing(boxes, container):
    container_w, container_h, container_d = container
    placements = []  # Kutuların yerleşim bilgisi

    # 📌 Kutuları büyükten küçüğe sıralıyoruz
    boxes.sort(key=lambda b: max(b[0], b[1], b[2]), reverse=True)  # En uzun kenara göre sırala

    # 📌 Mevcut boş alanları takip edelim
    free_spaces = [(0, 0, 0, container_w, container_h, container_d)]  # (x, y, z, w, h, d)

    for box in boxes:
        box_w, box_h, box_d = box
        best_index = None
        min_waste = float('inf')

        # 📌 En iyi boşluğu bul
        for i, (x, y, z, free_w, free_h, free_d) in enumerate(free_spaces):
            if box_w <= free_w and box_h <= free_h and box_d <= free_d:  # Sığabiliyor mu?
                waste = (free_w * free_h * free_d) - (box_w * box_h * box_d)  # Boşluk ne kadar azalıyor?
                if waste < min_waste:  # Daha iyi bir yer varsa güncelle
                    min_waste = waste
                    best_index = i

        # 📌 Eğer en iyi boşluğu bulduysak, oraya yerleştir
        if best_index is not None:
            x, y, z, free_w, free_h, free_d = free_spaces.pop(best_index)
            placements.append({'box': box, 'position': (x, y, z)})

            # 📌 Kalan boşlukları ekleyelim
            free_spaces.append((x + box_w, y, z, free_w - box_w, free_h, free_d))  # Sağ boşluk
            free_spaces.append((x, y + box_h, z, box_w, free_h - box_h, free_d))  # Alt boşluk
            free_spaces.append((x, y, z + box_d, box_w, box_h, free_d - box_d))  # Derinlik boşluğu
        else:
            print(f"❌ Konteyner dolu! {box} kutusu yerleştirilemedi.")

    return placements


def genetic_algorithm(boxes, container, generations=50, population_size=10, mutation_rate=0.1):
    def fitness(placements):
        total_used_volume = sum(box[0] * box[1] * box[2] for box in [p['box'] for p in placements])
        container_volume = container[0] * container[1] * container[2]
        return total_used_volume / container_volume
    
    population = [random.sample(boxes, len(boxes)) for _ in range(population_size)]
    
    for _ in range(generations):
        scored_population = [(first_fit_decreasing(individual, container), individual) for individual in population]
        scored_population.sort(key=lambda x: fitness(x[0]), reverse=True)
        selected_population = [ind for _, ind in scored_population[:population_size // 2]]

        children = []
        while len(children) < population_size:
            p1, p2 = random.sample(selected_population, 2)
            child = p1[:len(p1)//2] + p2[len(p2)//2:]
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]
            children.append(child)

        population = children

    best_solution = max(scored_population, key=lambda x: fitness(x[0]))
    return best_solution[0]



def pack_boxes(container, boxes):
    container_w, container_h, container_d = container
    yerlesen = []
    x, y, z = 0, 0, 0
    current_row_height = 0
    current_layer_depth = 0
    

    for box in boxes:
        box_w, box_h, box_d = box
        
        if x + box_w > container_w:
            x = 0
            y += current_row_height
            current_row_height = 0
        
        if y + box_h > container_h:
            y = 0
            z += current_layer_depth
            current_layer_depth = 0
        
        if z + box_d > container_d:
            print(f"Konteyner dolu! {box} kutusu yerleştirilemedi.")
            continue
        
        yerlesen.append({'box': box, 'position': (x, y, z)})
        x += box_w
        current_row_height = max(current_row_height, box_h)
        current_layer_depth = max(current_layer_depth, box_d)
    
    return yerlesen

# 📌 5. Kutuları Çizen Fonksiyon
def draw_box(ax, x, y, z, dx, dy, dz, color='cyan', edge_color='black', alpha=0.7):
    """ 3D kutu çizen fonksiyon """
    vertices = np.array([
        [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
        [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]
    ])
    
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[3], vertices[7], vertices[4]]
    ]
    
    box_poly = Poly3DCollection(faces, facecolors=color, edgecolors=edge_color, alpha=alpha)
    ax.add_collection3d(box_poly)

# 📌 6. 3D Grafik Çizme Fonksiyonu
def plot_placements(container, placements):
    """ Konteynerin ve kutuların 3D olarak çizildiği fonksiyon. """
    container_w, container_h, container_d = container
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 📌 Konteyneri çiziyoruz (şeffaf gri)
    draw_box(ax, 0, 0, 0, container_w, container_h, container_d, color='lightgrey', edge_color='black', alpha=0.3)

    # 📌 Kutuların çizimi
    colors = ['blue', 'red', 'purple', 'green', 'black', 'brown', 'orange']
    for i, placement in enumerate(placements):
        box = placement['box']
        pos = placement['position']
        draw_box(ax, *pos, *box, color=colors[i % len(colors)], edge_color='k', alpha=0.7)

    # 📌 Eksen ayarları (KUTULARI GERÇEK BOYUTLARINDA GÖSTERMEK İÇİN)
    ax.set_xlabel('X ekseni')
    ax.set_ylabel('Y ekseni')
    ax.set_zlabel('Z ekseni')
    ax.set_xlim(0, container_w)
    ax.set_ylim(0, container_h)
    ax.set_zlim(0, container_d)
    ax.set_title("Konteyner ve Yerleştirilen Kutular")

    # 📌 3D GRAFİĞİ GERÇEK BOYUT ORANLARINA GETİRME (ÖNEMLİ!)
    ax.set_box_aspect([container_w, container_h, container_d])  # 🔥 Kutuların oranlarını korur

    # 📌 Kamera açısını değiştirerek daha iyi görüntü sağla
    ax.view_init(elev=40, azim=135)


    
    plt.show()


if __name__ == "__main__":
    container, boxes = get_user_input()

    while True:
        algorithm_choice = choose_algorithm()
        
        if algorithm_choice is None:  # Kullanıcı çıkış yaparsa None dönecek
            break

        if algorithm_choice == 1:
            print("\n🚀 First Fit Decreasing (FFD) Algoritması Çalıştırılıyor...")
            placements = first_fit_decreasing(boxes, container)
        elif algorithm_choice == 2:
            print("\n🚀 Best Fit Decreasing (BFD) Algoritması Çalıştırılıyor...")
            placements = best_fit_decreasing(boxes, container)
        elif algorithm_choice == 3:
            print("\n🚀 Genetic Algorithm (GA) Çalıştırılıyor...")
            placements = genetic_algorithm(boxes, container)

        plot_placements(container, placements)  # Sonucu 3D olarak göster

    print("📌 Program başarıyla sonlandırıldı.")