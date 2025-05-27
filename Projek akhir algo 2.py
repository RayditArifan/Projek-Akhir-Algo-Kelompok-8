from collections import OrderedDict
from collections import deque

import csv
import os

USERS_FILE = "user.csv"
ADMIN_FILE = "admin.csv"

def initialize_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'kode tiket', 'role'])

    elif not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'role'])
            writer.writerow(['admin', 'admin123', 'admin']) 

def menu_utama ():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")
    print("              SELAMAT DATANG di PATHFINDER              ")
    print("")
    print ('')
    print ('1. User')
    print ('2. Admin')
    a = input ("Pilih Nomor: ")
    if a == '1' :
        login ()
    elif a == '2' :
        login_admin ()
    else:
        print ('Nomor yang anda masukkan salah !')
        menu_utama ()

def login():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("")
    print("              SELAMAT DATANG di PATHFINDER              ")
    print("_______________________ LOGIN __________________________")

    username = input("Masukkan username: ").strip()
    kode_tiket = input("Masukkan kode tiket: ").strip()

    with open(USERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['kode tiket'] == kode_tiket:
                print(f"Selamat datang, {username}!")
                if row['role'] == 'user':
                    pelanggan_menu ()
                return
    print("Login gagal! Username atau kode tiket salah.")
    print ('')
    print ('1. Coba Lagi')
    print ('2. Kembali')
    b = input ('Masukkan Nomor: ')
    if b == '1':
        login ()
    elif b == '2':
        menu_utama ()
    else:
        print ('Nomor yang anda masukkan salah !')
        login ()

def login_admin ():
    os.system ('cls')
    print("")
    print("              SELAMAT DATANG di PATHFINDER              ")
    print("_______________________ LOGIN __________________________")

    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    with open(ADMIN_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                print(f"Selamat datang, {username}!")
                if row['role'] == 'admin':
                    admin_menu()
                return
    print("Login gagal! Username atau password.")
    login_admin ()

def admin_menu():
    os.system ('cls')
    while True:
        print("\n--- MENU ADMIN ---")
        print("1. Tambah Data Pelanggan")
        print("2. Logout")
        a = input("Pilih menu: ")
        if a == '1':
            tambah_pelanggan()
        elif a == '2':
            menu_utama ()
        else:
            print("Pilihan tidak valid.")
        admin_menu ()

def tambah_pelanggan():
    os.system ('cls')
    username = input("Masukkan username pelanggan: ").strip()
    if not username:
        print("Username tidak boleh kosong!")
        input("Tekan ENTER untuk kembali...")
        tambah_pelanggan()
        return
    kode = input("Masukkan kode tiket: ").strip()
    if not kode:
        print("Kode tiket tidak boleh kosong!")
        input("Tekan ENTER untuk kembali...")
        tambah_pelanggan()
        return
    
    with open(USERS_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                print(f"[GAGAL] Username '{username}' sudah terdaftar.")
                input("Tekan ENTER untuk kembali...")
                tambah_pelanggan ()
                return
            
    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, kode, 'user'])
    print(f"Data pelanggan '{username}' berhasil ditambahkan.")
    a = input ('klik enter untuk lanjut')
    admin_menu()

PathFinder_map = {
    'Gerbang Utama': ['Rumah Hantu', 'Tornado', 'Halilintar'],
    'Rumah Hantu': ['Kicir-Kicir'],
    'Tornado': ['Hysteria'],
    'Halilintar': ['Bianglala'],
    'Kicir-Kicir': ['Istana Boneka'],
    'Hysteria': ['Gajah Bledug'],
    'Bianglala': ['Komidi Putar'],
    'Istana Boneka': ['Dunia Kartun'],
    'Gajah Bledug': ['Arung Jeram'],
    'Komidi Putar': ['Kora-Kora'],
    'Dunia Kartun': ['Niagara'],
    'Arung Jeram': [],
    'Kora-Kora': [],
    'Niagara': ['Rumah Miring'],
    'Rumah Miring': ['Ontang-Anting'],
    'Ontang-Anting': []
}

nama_wahana_lower_map = {nama.lower(): nama for nama in PathFinder_map}

def bfs(start, goal):
    visited = set()
    queue = deque([[start]])

    if start == goal:
        return [start]

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            for neighbor in PathFinder_map.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

                if neighbor == goal:
                    return new_path
            visited.add(node)
    return None

def pelanggan_menu():
    os.system ('cls')
    print("===== Selamat Datang di Aplikasi PathFinder =====\n")
    print("Daftar wahana yang tersedia:")
    for wahana in PathFinder_map:
        print("-", wahana)
    print("\nSilakan masukkan nama wahana sesuai daftar di atas.\n")

    start_input = input("Masukkan titik awal: ").strip().lower()
    goal_input = input("Masukkan tujuan akhir: ").strip().lower()

    if start_input not in nama_wahana_lower_map or goal_input not in nama_wahana_lower_map:
        print("\nTitik awal atau tujuan tidak valid. Silakan coba lagi.")
        return

    start = nama_wahana_lower_map[start_input]
    goal = nama_wahana_lower_map[goal_input]

    route = bfs(start, goal)

    if route:
        print(f"\nRute terbaik dari '{start}' ke '{goal}':")
        for i, step in enumerate(route):
            print(f"  {i+1}. {step}")
        print(f"\nTotal langkah: {len(route)-1} wahana")
        pelanggan_menu()
    else:
        print(f"\nTidak ditemukan jalur dari '{start}' ke '{goal}'.")
        input ('ketik enter untuk kembali')
        pelanggan_menu ()


# ======== MAIN PROGRAM ========
initialize_files()
menu_utama()

# Peta awal
PathFinder_map = OrderedDict({
    'Gerbang Utama': ['Bianglala', 'Istana Boneka'],
    'Bianglala': ['Tornado', 'Halilintar'],
    'Istana Boneka': ['Rumah Miring', 'Niagara'],
    'Tornado': ['Arung Jeram'],
    'Halilintar': [],
    'Rumah Miring': [],
    'Niagara': ['Kora-Kora'],
    'Kora-Kora': [],
    'Arung Jeram': []
})

#Fitur Admint nambah node
def tambah_node_di_posisi(peta, nama_node_baru, tujuan=[], posisi=0):
    if nama_node_baru in peta:
        print(f"Node '{nama_node_baru}' sudah ada.")
        return

    items = list(peta.items())
    posisi = max(0, min(posisi, len(items)))  # batasi agar tetap dalam range
    items.insert(posisi, (nama_node_baru, tujuan))
    
    peta_baru = OrderedDict(items)
    peta.clear()
    peta.update(peta_baru)

def tampilkan_peta(peta):
    print("\n=== PathFinder Map Saat Ini ===")
    for i, (lokasi, tujuan) in enumerate(peta.items()):
        print(f"{i}. {lokasi} ➜ {tujuan}")
    print()

def menu_tambah_node():
    while True:
        tampilkan_peta(PathFinder_map)

        nama = input("Masukkan nama node baru (atau 'exit' untuk keluar): ").strip()
        if nama.lower() == 'exit':
            break

        tujuan_input = input("Masukkan tujuan (dipisah koma, contoh: Halilintar,Kora-Kora): ").strip()
        tujuan = [x.strip() for x in tujuan_input.split(',') if x.strip()]

        try:
            posisi = int(input("Masukkan indeks posisi penyisipan (0 untuk awal): ").strip())
        except ValueError:
            print("Input posisi tidak valid. Disisipkan di akhir.")
            posisi = len(PathFinder_map)

        tambah_node_di_posisi(PathFinder_map, nama, tujuan, posisi)

print("\nPeta akhir:")
