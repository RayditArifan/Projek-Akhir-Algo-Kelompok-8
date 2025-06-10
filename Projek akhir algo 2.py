from collections import deque
import csv
import os

USERS_FILE = "user.csv"
ADMIN_FILE = "admin.csv"
MAP_FILE = "map.csv"

def initialize_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'kode tiket', 'role'])
            writer.writerows(['Aby', '123', 'pelanggan'])

    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password', 'role'])
            writer.writerow(['admin', 'admin123', 'admin'])

    if not os.path.exists(MAP_FILE): 
        with open(MAP_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['from', 'to'])
            writer.writerows([
                ['Gerbang Utama', 'Rumah Hantu'],
                ['Gerbang Utama', 'Tornado'],
                ['Gerbang Utama', 'Halilintar'],
                ['Rumah Hantu', 'Kicir Kicir'],
                ['Tornado', 'Hysteria'],
                ['Halilintar', 'Bianglala'],
                ['Kicir Kicir', 'Istana Boneka'],
                ['Hysteria', 'Gajah Bledug'],
                ['Bianglala', 'Komidi Putar'],
                ['Istana Boneka', 'Dunia Kartun'],
                ['Gajah Bledug', 'Arung Jeram'],
                ['Komidi Putar', 'Kora Kora'],
                ['Dunia Kartun', 'Niagara'],
                ['Niagara', 'Rumah Miring'],
                ['Rumah Miring', 'Ontang Anting'],
                ['Ontang Anting', 'Gerbang Utama'],
                ['Kora Kora', 'Gerbang Utama'],
                ['Arung Jeram', 'Dunia Kartun'],
            ])

def pathfinder_map():
    graph = {}
    if not os.path.exists(MAP_FILE):
        print(f"File '{MAP_FILE}' tidak ditemukan.")
        return graph

    with open(MAP_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            start = row['from']
            end = row['to']
            if start not in graph:
                graph[start] = []
            graph[start].append(end)
            if end not in graph:
                graph[end] = []
    return graph

PathFinder_map = pathfinder_map()
nama_wahana_lower_map = {nama.lower(): nama for nama in PathFinder_map}

def menu_utama():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n==================================================")
    print("         SELAMAT DATANG DI APLIKASI PATHFINDER     ")
    print("==================================================")
    print("1. Login sebagai User")
    print("2. Login sebagai Admin")
    print("0. Keluar")
    choice = input("Pilih menu: ")

    if choice == '1':
        login_user()
    elif choice == '2':
        login_admin()
    elif choice == '0':
        print("Terima kasih telah menggunakan PathFinder😍")
        exit()
    else:
        print("Maaf, pilihan tidak tersedia😔")
        input("Tekan enter untuk kembali")
        menu_utama()

def login_user():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n============== LOGIN USER ==============")
    username = input("Masukkan username: ").strip()
    kode_tiket = input("Masukkan kode tiket: ").strip()

    with open(USERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['kode tiket'] == kode_tiket:
                print(f"\nSelamat datang, {username}😊\n")
                pelanggan_menu()
                return
    print("\nMaaf, Username atau kode tiket salah ")
    input("Tekan enter untuk kembali")
    menu_utama()

def login_admin():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n============== LOGIN ADMIN ==============")
    username = input("Masukkan username admin: ").strip()
    password = input("Masukkan password: ").strip()

    with open(ADMIN_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                print(f"\nSelamat datang, {username}!😊\n")
                admin_menu()
                return
    print("\nMaaf, Username atau password salah.")
    input("Tekan enter untuk kembali")
    menu_utama()

def admin_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n============== MENU ADMIN ==============")
        print("1. Tambah Data Pelanggan")
        print("2. Lihat Peta Wahana")
        print("3. Tambah titik rute")
        print("4. Hapus baris peta")  
        print("5. Logout")
        choice = input("Pilih menu: ")

        if choice == '1':
            tambah_pelanggan()
        elif choice == '2':
            tampilkan_peta()
            input("Tekan enter untuk kembali")
        elif choice == '3':
            tambah_titik_rute()
        elif choice == '4':
            try:
                print("\n--- Hapus Baris Peta ---")
                row_index = int(input("Masukkan index baris yang ingin dihapus: "))
                hapus_baris_peta(row_index)
            except ValueError:
                print("Index baris harus berupa angka.")
            input("Tekan enter untuk kembali")
        elif choice == '5':
            print("\nTerima kasih telah berkunjung Admin🥰\n")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan enter untuk kembali")

def tambah_pelanggan():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=========== TAMBAH DATA PELANGGAN ===========")
    username = input("Masukkan username pelanggan: ").strip()
    kode = input("Masukkan kode tiket: ").strip()

    if not username or not kode:
        print("Username dan kode tiket tidak boleh kosong!")
        input("Tekan enter untuk kembali")
        return

    with open(USERS_FILE, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username:
                print(f" Username '{username}' sudah terdaftar ")
                input("Tekan enter untuk kembali")
                return

    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, kode, 'user'])

    print(f"Data pelanggan '{username}' berhasil ditambahkan.")
    input("Tekan enter untuk kembali")

def insert_route_at_row(from_location, to_location, row_index, file_path=MAP_FILE):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' belum diinisialisasi.")

    with open(file_path, 'r', newline='') as file:
        reader = list(csv.reader(file))

    
    if row_index < 1 or row_index > len(reader):
        print(f"Row index harus antara 1 dan {len(reader)} (tidak bisa menimpa header).")
        return

    new_row = [from_location, to_location]

    
    reader.insert(row_index, new_row)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(reader)

    print(f"Route '{from_location}' → '{to_location}' berhasil disisipkan di baris ke-{row_index}.")

def tambah_titik_rute():
    print("\n--- Tambah Titik Peta ---")
    from_location = input("Masukkan lokasi FROM: ").strip()
    to_location = input("Masukkan lokasi TO: ").strip()

    try:
        row_index = int(input("Masukkan index baris untuk menyisipkan (mulai dari 1, setelah header): "))

        insert_route_at_row(from_location, to_location, row_index)

    except ValueError:
        print("Index baris harus berupa angka.")

    input("Tekan enter untuk kembali")

def hapus_baris_peta(row_index, file_path=MAP_FILE):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' tidak ditemukan.")
        return

    with open(file_path, 'r', newline='') as file:
        rows = list(csv.reader(file))

    if row_index < 1 or row_index >= len(rows):
        print(f"Index harus antara 1 dan {len(rows) - 1}. (Index 0 adalah header dan tidak boleh dihapus)")
        return

    removed = rows.pop(row_index)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Baris ke-{row_index} berhasil dihapus: {removed}")

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
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========== MENU PELANGGAN ===========")
        print("Daftar wahana yang tersedia:")
        for wahana in PathFinder_map:
            print("-", wahana)
        print("\nMasukkan nama wahana sesuai daftar.\n")

        start_input = input("Masukkan titik awal: ").strip().lower()
        goal_input = input("Masukkan tujuan akhir: ").strip().lower()

        if start_input not in nama_wahana_lower_map or goal_input not in nama_wahana_lower_map:
            print("\nTitik awal atau tujuan tidak valid")
            input("Tekan enter untuk coba lagi")
            continue

        start = nama_wahana_lower_map[start_input]
        goal = nama_wahana_lower_map[goal_input]
        route = bfs(start, goal)

        if route:
            print(f"\nRute terbaik dari '{start}' ke '{goal}':")
            for i, step in enumerate(route):
                print(f"  {i+1}. {step}")
            print(f"\nTotal langkah: {len(route)-1} wahana\n")
        else:
            print(f"\nTidak ditemukan jalur dari '{start}' ke '{goal}'.")

        while True:
            ulang = input("\nApakah ingin mencari rute lain? (y/n): ").strip().lower()
            if ulang == 'y':
                break
            elif ulang == 'n':
                print('TERIMA KASIH TELAH MENGGUNAKAN FITUR KAMI 🥰')
                return
            else:
                print("Input tidak valid! Masukkan hanya 'y' atau 'n'.")

def tampilkan_peta():
    if not os.path.exists(MAP_FILE):
        print(f"File '{MAP_FILE}' tidak ditemukan.")
        return

    with open(MAP_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        print("\n=========== PETA WAHANA (MAP) ===========")
        for i, row in enumerate(reader, start=1):
            if len(row) >= 2:
                print(f"{i}. {row[0]} → {row[1]}")
            else:
                print(f"{i}. Data tidak lengkap.")

initialize_files()
menu_utama()
