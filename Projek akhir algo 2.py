a = "hello world"
print(a)

print ("tes commit 2")
def tampilkan_graph(graph):
    print("\nGraph saat ini:")
    for node in graph:
        print(f"{node}: {graph[node]}")
    print()

def tambah_node(graph):
    parent = input("Masukkan nama node induk (yang akan ditambahkan anaknya): ")
    if parent not in graph:
        print(f"Node '{parent}' tidak ditemukan dalam graph.")
        return

    child = input("Masukkan nama node baru (anak dari " + parent + "): ")
    
    if child in graph:
        print(f"Node '{child}' sudah ada dalam graph.")
        return

    pos = input(f"Masukkan posisi penyisipan anak di '{parent}' (0 untuk awal, kosong untuk akhir): ")
    try:
        pos = int(pos)
    except:
        pos = len(graph[parent])

    graph[parent].insert(pos, child)
    graph[child] = []
    print(f"Node '{child}' berhasil ditambahkan sebagai anak dari '{parent}' pada posisi {pos}.")

def tambah_parent_node(graph):
    child = input("Masukkan nama node target yang ingin ditambahkan parent barunya: ")
    if child not in graph:
        print(f"Node '{child}' tidak ditemukan.")
        return

    new_parent = input("Masukkan nama parent node baru: ")
    if new_parent in graph:
        print(f"Node '{new_parent}' sudah ada.")
        return

    # Cari node yang memiliki 'child' sebagai anak
    found = False
    for node, children in graph.items():
        if child in children:
            tampilkan_graph(graph)
            pos = input(f"Masukkan posisi baru untuk '{new_parent}' dalam anak dari '{node}' (default akhir): ")
            try:
                pos = int(pos)
            except:
                pos = len(graph[node])
            # Ganti child dengan new_parent
            children.remove(child)
            children.insert(pos, new_parent)
            found = True
            break

    if not found:
        print(f"Node '{child}' tidak memiliki parent yang bisa ditemukan.")
        return

    # Tambahkan new_parent dan jadikan child sebagai anaknya
    graph[new_parent] = [child]
    print(f"Node parent baru '{new_parent}' berhasil ditambahkan di atas '{child}'.")

def tambah_admin():
    graph = {
        '0': ['N1', 'E1', 'S1'],
        'N1': ['N2'],
        'N2': ['N3'],
        'N3': ['N4'],
        'N4': ['N5'],
        'N5': [],
        'E1': ['E2'],
        'E2': ['E3'],
        'E3': ['E4'],
        'E4': ['E5'],
        'E5': [],
        'S1': ['S2'],
        'S2': ['S3'],
        'S3': ['S4'],
        'S4': ['S5'],
        'S5': []
    }

    while True:
        tampilkan_graph(graph)
        print("Menu:")
        print("1. Tambah child node")
        print("2. Tambah parent node")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")
        if pilihan == '1':
            tambah_node(graph)
        elif pilihan == '2':
            tambah_parent_node(graph)
        elif pilihan == '3':
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")
